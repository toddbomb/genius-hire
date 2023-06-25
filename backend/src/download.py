from flask import Blueprint, send_file

report = Blueprint('report', __name__, url_prefix="/report")

@report.route('/download', methods=['GET'])
def download_report():
    # Logic to generate the report file
    # ...

    report_path = "/Users/cristinconnerney/Desktop/restest.pdf"

    return send_file(report_path, attachment_filename='report.pdf', as_attachment=True)