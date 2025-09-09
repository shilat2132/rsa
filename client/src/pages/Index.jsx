
import { useNavigate } from 'react-router-dom';
import MainNavigation from '../components/MainNavigation';
import { Button } from '@/components/ui/button';
import SimulationCard from '../components/SimulationCard';
import HomeHeader from '../components/HomeHeader';

const Index = () => {
  const navigate = useNavigate();
  
  const simulations = [
    {
      title: 'Key Generation',
      description: 'Generate public and private keys for RSA encryption',
      path: '/key-generation',
      icon: 'key'
    },
    {
      title: 'Encryption',
      description: 'Encrypt a message using RSA encryption',
      path: '/encryption',
      icon: 'lock'
    },
    {
      title: 'Decryption',
      description: 'Decrypt a message using RSA decryption',
      path: '/decryption',
      icon: 'unlock'
    }
  ];
  
  return (
    <div className="min-h-screen bg-gradient-to-b from-white to-purple-50">
      <div className="container mx-auto px-4 py-10">
        <MainNavigation />
        
        <HomeHeader />
        
        <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mt-12">
          {simulations.map((sim) => (
            <SimulationCard
              key={sim.path}
              title={sim.title}
              description={sim.description}
              icon={sim.icon}
              onClick={() => navigate(sim.path)}
            />
          ))}
        </div>
      </div>
    </div>
  );
};

export default Index;
