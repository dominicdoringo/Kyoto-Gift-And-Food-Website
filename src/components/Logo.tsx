import { HandCoins } from 'lucide-react';
import Link from 'next/link';

const Logo = () => {
	return (
		<Link
			href="/"
			className="flex items-center gap-2"
		>
			<HandCoins className="stroke h-11 w-11 stroke-amber-500 stroke-[1.5]" />
			<p className="bg-gradient-to-r from-amber-400 to-orange-500 bg-clip-text text-3xl font-bold leading-tight tracking-tighter text-transparent">
				Budget Buddy
			</p>
		</Link>
	);
};

export const LogoMobile = () => {
	return (
		<Link
			href="/"
			className="flex items-center gap-2"
		>
			<p className="bg-gradient-to-r from-amber-400 to-orange-500 bg-clip-text text-3xl font-bold leading-tight tracking-tighter text-transparent">
				Budget Buddy
			</p>
		</Link>
	);
};

export default Logo;
