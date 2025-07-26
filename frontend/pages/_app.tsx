import type { AppProps } from 'next/app'
import '../styles/globals.css'
import { NotificationProvider } from '../components/NotificationSystem'

export default function App({ Component, pageProps }: AppProps) {
  return (
    <NotificationProvider>
      <Component {...pageProps} />
    </NotificationProvider>
  )
} 