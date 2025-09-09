
import { Link } from 'react-router-dom';
import { Button } from '@/components/ui/button';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';

const SimulationCard = ({ title, description, content, linkTo, linkText }) => {
  return (
    <Card className="hover:shadow-lg transition-shadow">
      <CardHeader className="bg-blue-100 rounded-t-lg">
        <CardTitle>{title}</CardTitle>
        <CardDescription>{description}</CardDescription>
      </CardHeader>
      <CardContent className="pt-6">
        <p className="mb-6 text-gray-700">
          {content}
        </p>
        <Link to={linkTo}>
          <Button className="w-full">
            {linkText}
          </Button>
        </Link>
      </CardContent>
    </Card>
  );
};

export default SimulationCard;
