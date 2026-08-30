import Navbar from "./components/Navbar";
import Hero from "./components/Hero";
import Features from "./components/Features";
import HowItWorks from "./components/HowItWorks";
import Privacy from "./components/Privacy";
import Screenshots from "./components/Screenshots";
import UserGuide from "./components/UserGuide";
import Download from "./components/Download";
import GitHubSection from "./components/GitHubSection";
import FAQ from "./components/FAQ";
import Footer from "./components/Footer";

export default function App() {
  return (
    <div className="min-h-screen bg-base-950">
      <Navbar />
      <main>
        <Hero />
        <Features />
        <HowItWorks />
        <Privacy />
        <Screenshots />
        <UserGuide />
        <Download />
        <GitHubSection />
        <FAQ />
      </main>
      <Footer />
    </div>
  );
}
