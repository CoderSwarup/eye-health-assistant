import { Navigation } from '@/components/layout/Navigation';
import { Footer } from '@/components/layout/Footer';
import { Hero } from '@/components/sections/Hero';
import { Features } from '@/components/sections/Features';
import { SmartMonitoring } from '@/components/sections/SmartMonitoring';
import { TimerMode } from '@/components/sections/TimerMode';
import { Privacy } from '@/components/sections/Privacy';
import { Exercises } from '@/components/sections/Exercises';
import { Statistics } from '@/components/sections/Statistics';
import { HowItWorks } from '@/components/sections/HowItWorks';
import { EyeCare } from '@/components/sections/EyeCare';
import { CrossPlatform } from '@/components/sections/CrossPlatform';
import { FAQ } from '@/components/sections/FAQ';
import { DownloadCTA } from '@/components/sections/DownloadCTA';

export default function Home() {
  return (
    <>
      <Navigation />
      <main>
        <Hero />
        <Features />
        <SmartMonitoring />
        <TimerMode />
        <Privacy />
        <Exercises />
        <Statistics />
        <HowItWorks />
        <EyeCare />
        <CrossPlatform />
        <FAQ />
        <DownloadCTA />
      </main>
      <Footer />
    </>
  );
}
