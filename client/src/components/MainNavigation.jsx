
import { useNavigate, useLocation } from 'react-router-dom';
import { 
  NavigationMenu,
  NavigationMenuList,
  NavigationMenuItem,
  NavigationMenuLink,
  navigationMenuTriggerStyle
} from '@/components/ui/navigation-menu';
import { cn } from '@/lib/utils';

import styles from '../styles/homepage.module.css'

const MainNavigation = () => {
  const navigate = useNavigate();
  const location = useLocation();
  
  const isActive = (path) => location.pathname === path;
  
  const handleNavigate = (path) => (e) => {
    e.preventDefault();
    navigate(path);
  };
  
  return (
    <NavigationMenu className="max-w-full w-full justify-start mb-6">
      <NavigationMenuList className="space-x-2">
        <NavigationMenuItem>
          <NavigationMenuLink
            className={`${styles.tabs} ${cn(
              navigationMenuTriggerStyle(),
              isActive('/') && 'bg-accent text-accent-foreground'
            )}`}
            onClick={handleNavigate('/')}
          >
            Home
          </NavigationMenuLink>
        </NavigationMenuItem>
        
        <NavigationMenuItem>
          <NavigationMenuLink
            className={`${styles.tabs} ${cn(
              navigationMenuTriggerStyle(),
              isActive('/key-generation') && 'bg-accent text-accent-foreground'
            )}`}
            onClick={handleNavigate('/key-generation')}
          >
            Key Generation
          </NavigationMenuLink>
        </NavigationMenuItem>
        
        <NavigationMenuItem>
          <NavigationMenuLink
            className={`${styles.tabs} ${cn(
              navigationMenuTriggerStyle(),
              isActive('/encryption') && 'bg-accent text-accent-foreground'
            )}`}
            onClick={handleNavigate('/encryption')}
          >
            Encryption
          </NavigationMenuLink>
        </NavigationMenuItem>
        
        <NavigationMenuItem>
          <NavigationMenuLink
            className={`${styles.tabs} ${cn(
              navigationMenuTriggerStyle(),
              isActive('/decryption') && 'bg-accent text-accent-foreground'
            )}`}
            onClick={handleNavigate('/decryption')}
          >
            Decryption
          </NavigationMenuLink>
        </NavigationMenuItem>
      </NavigationMenuList>
    </NavigationMenu>
  );
};

export default MainNavigation;
