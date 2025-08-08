import type { Metadata } from "next";
import { SessionProvider } from "@/contexts/SessionContext"
import { NavBar } from "@/components/NavBar";
import { ThemeProvider } from "@/components/theme-provider";
import "./globals.css";

// import { Geist, Geist_Mono } from "next/font/google";

// const geistSans = Geist({
//   variable: "--font-geist-sans",
//   subsets: ["latin"],
// });

// const geistMono = Geist_Mono({
//   variable: "--font-geist-mono",
//   subsets: ["latin"],
// });

export const metadata: Metadata = {
  title: "Leadership Coach",
  description: "A platform to enhance leadership skills",
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    // <html lang="en">
    <html lang="en" suppressHydrationWarning className="">

      <body>
      <ThemeProvider 
      attribute="class" 
      defaultTheme="system" 
      enableSystem
      disableTransitionOnChange
      >
      <SessionProvider>
        {/* <style jsx global>{`
          :root {
            --font-geist-sans: ${geistSans.style.fontFamily};
            --font-geist-mono: ${geistMono.style.fontFamily};
          }
        `}</style> */}
        <NavBar />
        <main>{children}</main>
      </SessionProvider>
      </ThemeProvider>
      </body>
    </html>
  );
}
