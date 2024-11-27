'use client';

import { Button } from '@/components/ui/button';
import { Card, CardContent, CardFooter } from '@/components/ui/card';
import Image from 'next/image';

interface FeaturedItemProps {
	name: string;
	price: number;
	description: string;
	imageUrl: string;
}

export function FeaturedItemCard({
	name,
	price,
	description,
	imageUrl,
}: FeaturedItemProps) {
	return (
		<Card className="w-[300px] flex flex-col">
			<CardContent className="pt-4">
				<div className="relative w-full h-[200px] mb-4">
					<Image
						src={imageUrl}
						alt={name}
						fill
						className="object-cover rounded-md"
					/>
				</div>
				<h3 className="font-semibold text-lg mb-2">{name}</h3>
				<p className="text-sm text-muted-foreground mb-2">{description}</p>
				<p className="text-lg font-bold">${price.toFixed(2)}</p>
			</CardContent>
			<CardFooter className="mt-auto">
				<Button className="w-full bg-[#59d473] hover:bg-[#429b58]">
					Add to Cart
				</Button>
			</CardFooter>
		</Card>
	);
}
