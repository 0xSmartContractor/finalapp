import { ClerkProvider } from "@clerk/nextjs";
import Navbar from "../components/marketing/Navbar";

export default function MarketingLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <ClerkProvider>
      <Navbar />
      {children}
    </ClerkProvider>
  );
}
