import { ReactNode } from 'react';
import { MutableRefObject, useState } from 'react';

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

const OpenCloseButton = ({ onClick, side }: { onClick: () => void, side: 'left' | 'right' }) => {
  return (
    <button className={`fixed top-4 ${side}-4 z-40 bg-white rounded-lg shadow-md dark:bg-[#343541] dark:text-white p-2`} onClick={onClick}>
      {/* Add button icon here */}
    </button>
  );
};

const MyComponent = <T,>({
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
  const [isSidebarOpen, setIsSidebarOpen] = useState<boolean>(isOpen);

  const toggleSidebar = () => {
    setIsSidebarOpen(!isSidebarOpen);
  };

  return (
    <div>
      {/* Rest of your component code */}
      {isSidebarOpen ? (
        <div>
          {/* Sidebar content */}
        </div>
      ) : (
        <OpenCloseButton onClick={toggleSidebar} side={side} />
      )}
    </div>
  );
};

export default MyComponent;
