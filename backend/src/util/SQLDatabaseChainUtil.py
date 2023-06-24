from langchain.prompts.prompt import PromptTemplate
from langchain import OpenAI, SQLDatabase, SQLDatabaseChain

def getSQLChainAnswer(question, db, chat_history):
    prompt_template = '''
    Your job is to answer the question below, delimited by triple backticks, using the following tables {table_info} and {dialect}. Keep in mind that in order to   



Here are some examples:
User: What is the highest performance for Rugs USA?
AI: SELECT * FROM (SELECT campaigns.ad_name, SUM(performance_data.impressions) AS impressions, CASE WHEN SUM(performance_data.impressions) = 0 THEN Null ELSE SUM(performance_data.clicks) / SUM(performance_data.impressions) END AS CTR,
CASE WHEN SUM(performance_data.clicks) = 0 THEN Null ELSE SUM(performance_data.cpc * performance_data.clicks) / SUM(performance_data.clicks) END AS CPC
FROM  performance_data
INNER JOIN campaigns ON performance_data.campaign_id = campaigns.id
where campaigns.advertiser_id = 33
group by campaigns.ad_name
order by impressions desc) sub  WHERE CTR IS NOT NULL AND CPC IS NOT NULL order by CTR desc

User: What is the lowest performance for Rugs USA?
AI: SELECT * FROM (SELECT campaigns.ad_name, SUM(performance_data.impressions) AS impressions, CASE WHEN SUM(performance_data.impressions) = 0 THEN Null ELSE SUM(performance_data.clicks) / SUM(performance_data.impressions) END AS CTR,
CASE WHEN SUM(performance_data.clicks) = 0 THEN Null ELSE SUM(performance_data.cpc * performance_data.clicks) / SUM(performance_data.clicks) END AS CPC
FROM  performance_data
INNER JOIN campaigns ON performance_data.campaign_id = campaigns.id
where campaigns.advertiser_id = 33
group by campaigns.ad_name
order by impressions) sub WHERE CTR IS NOT NULL AND CPC IS NOT NULL order by CTR

User: What is the highest performance for Rugs USA from 2019-01-01 to 2022-01-02?
AI:SELECT * FROM (SELECT campaigns.ad_name, SUM(performance_data.impressions) AS impressions, CASE WHEN SUM(performance_data.impressions) = 0 THEN Null ELSE SUM(performance_data.clicks) / SUM(performance_data.impressions) END AS CTR,
CASE WHEN SUM(performance_data.clicks) = 0 THEN Null ELSE SUM(performance_data.cpc * performance_data.clicks) / SUM(performance_data.clicks) END AS CPC
FROM  performance_data
INNER JOIN campaigns ON performance_data.campaign_id = campaigns.id
where campaigns.advertiser_id = 33
and performance_data.date between '2019-01-01' and '2022-01-02'
group by campaigns.ad_name
order by impressions desc) sub  WHERE CTR IS NOT NULL AND CPC IS NOT NULL order by CTR desc

Question: {input} 
    '''

    prompt = PromptTemplate(
        input_variables=["input", "table_info", "dialect"], template=prompt_template
        )
    # session = Session(name='test-example')
    # llm = LangChainLLMs(llm=OpenAI(temperature=0))
    from langchain.chat_models import ChatOpenAI
    llm = ChatOpenAI(temperature=0, model_name='gpt-3.5-turbo-16k')
    # from langchain.llms import VertexAI
    # llm = VertexAI()
    db_chain = SQLDatabaseChain.from_llm(llm, db, prompt=prompt, verbose=True, memory=chat_history)
    # llm = LangChainLLMs(llm=OpenAI(temperature=0, verbose=True), session=session)
    return db_chain.run(question)
