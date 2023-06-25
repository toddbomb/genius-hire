import { IconFolderPlus, IconMistOff, IconPlus } from '@tabler/icons-react';
import { ReactNode } from 'react';
import { useTranslation } from 'react-i18next';
import FileUploadArea from "@/components/File/FileUploadArea"; //"../components/File/FileUploadArea";
import TextInputArea from "@/components/File/TextInput"; 
import FileDownloadArea from "@/components/File/FileDownloadArea"; 
import ToggleButton from "@/components/File/toggle"
import { FileLite } from "@/types/file";
import Head from "next/head";
import DbUploadArea from "@/components/File/DbUploadArea"; 
import { ChevronUpIcon } from "@heroicons/react/24/outline";
import { PluginSelect } from '@/components/Chat/PluginSelect';
import { Plugin } from '@/types/plugin';

import {
  IconBolt,
  IconBrandGoogle,
} from '@tabler/icons-react';
import {
  MutableRefObject,
  useState,
} from 'react';

import {
  CloseSidebarButton,
  OpenSidebarButton,
} from './components/OpenCloseButton';

interface Props<T> {
  isOpen: boolean;
  side: 'left' | 'right';
  items: T[];
  itemComponent: ReactNode;
  folderComponent: ReactNode;
  footerComponent?: ReactNode;
  addItemButtonTitle: string;
  searchTerm: string;
  handleSearchTerm: (searchTerm: string) => void;
  toggleOpen: () => void;
  handleCreateItem: () => void;
  handleCreateFolder: () => void;
  handleDrop: (e: any) => void;
  textareaRef: MutableRefObject<HTMLTextAreaElement | null>;
}


const Sidebar = <T,>({
  isOpen,
  side,
  items,
  itemComponent,
  folderComponent,
  footerComponent,
  addItemButtonTitle,
  searchTerm,
  handleSearchTerm,
  toggleOpen,
  handleCreateItem,
  handleCreateFolder,
  handleDrop,
  textareaRef,
}: Props<T>) => {
  const { t } = useTranslation('promptbar');

  const allowDrop = (e: any) => {
    e.preventDefault();
  };

  const highlightDrop = (e: any) => {
    e.target.style.background = '#343541';
  };

  const removeHighlight = (e: any) => {
    e.target.style.background = 'none';
  };

  const [files, setFiles] = useState<FileLite[]>([]);
  const [showPluginSelect, setShowPluginSelect] = useState(false);
  const [plugin, setPlugin] = useState<Plugin | null>(null);
  const [isTyping, setIsTyping] = useState<boolean>(false);

  return (
    <div>
      <div className={`sticky top-10 fixed z-40 flex h-full w-[300px] flex-none flex-col space-y-2 bg-[#181817] p-2 text-[14px] transition-all sm:relative sm:top-0 rounded shadow`}>

{/*       <div className="flex items-center pt-5 ml-5 mr-5">
          <span className="text-[16px] font-semibold text-gray-800">
              Select Model:
          </span>
        </div> */}


        <div className="flex items-center pl-5 pr-5 pt-2 pb-8">

                  <img src="logo1.png" width="160" height="20"/>

        </div>

        <div className="flex items-center mb-12 ml-5 mr-5">
          <span className="text-[16px] font-semibold text-white" style={{ fontFamily: 'Roboto Mono, sans-serif' }}>
            
            Welcome to HR-IQ!
          </span>
        </div>

        <div className="flex items-center pt-3 mb-12 ml-6 mr-6">
          <span className="text-[12px] text-white text-sm" style={{ fontFamily: 'Roboto Mono, sans-serif' }}>
            Upload resumes and a job description, and let our intelligent chatbot analyze the data,
            generate reports, and provide customized interview questions.
          </span>
        </div>

        <div className="flex items-center pt-5 ml-5 mr-5">
          <FileUploadArea
            handleSetFiles={setFiles}
            maxNumFiles={75}
            maxFileSizeMB={30}
          />
        </div>
      
        <div className="flex items-center pt-5 ml-5 mr-5">
          <TextInputArea/>
        </div>

        <div className="flex items-center pt-10 ml-5 mr-5">
          <span className="text-[16px] font-semibold text-white" style={{fontFamily: 'Roboto Mono, sans-serif'}}>
            Not hiring right now? 
          </span>
        </div>

        <div className="flex items-center mb-6 pt-3  pr-2 ml-5 mr-5">
          <span className="text-[12px] text-white text-sm" style={{ fontFamily: 'Roboto Mono, sans-serif' }}>
            That's okay. You can test HR-IQ with some resumes we have on file. 
          </span>

          <ToggleButton />
        </div>

        <div className="flex items-center pt-5 ml-5 mr-5">
          <FileDownloadArea/>
        </div>

      {/* {footerComponent} */}
      </div>
    </div>
  );
}
export default Sidebar;
