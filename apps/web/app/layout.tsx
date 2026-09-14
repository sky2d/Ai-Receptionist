import './globals.css';

export const metadata = {
  title: 'AI Receptionist',
  description: 'Manage your AI Receptionist Platform',
}

export default function RootLayout({
  children,
}: {
  children: React.ReactNode
}) {
  return (
    <html lang="en">
      <body>{children}</body>
    </html>
  )
}
