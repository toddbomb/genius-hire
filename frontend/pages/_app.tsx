import { Toaster } from 'react-hot-toast';
import { QueryClient, QueryClientProvider } from 'react-query';

import { appWithTranslation } from 'next-i18next';
import type { AppProps } from 'next/app';
import { Inter } from 'next/font/google';

import '@/styles/globals.css';
import { ClerkProvider, SignedIn, SignedOut, SignIn, UserButton } from '@clerk/nextjs';

const inter = Inter({ subsets: ['latin'] });

function App({ Component, pageProps }: AppProps<{}>) {
  const queryClient = new QueryClient();

  return (
    <div className={inter.className}>
      <Toaster />
      <ClerkProvider>
        <SignedIn>
          <UserButton afterSignOutUrl="/"/>
          <QueryClientProvider client={queryClient}>
          <Component {...pageProps} />
        </QueryClientProvider>
        </SignedIn>
        <SignedOut>
          <SignIn />
        </SignedOut>
      </ClerkProvider>
    </div>
  );
}

export default appWithTranslation(App);
