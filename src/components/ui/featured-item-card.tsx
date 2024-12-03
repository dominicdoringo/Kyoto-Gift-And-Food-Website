'use client';

import { Button } from '@/components/ui/button';
import { Card, CardContent, CardFooter } from '@/components/ui/card';
import Image from 'next/image';
import Link from 'next/link';
import { Product } from '@/lib/types';

interface FeaturedItemProps {
	id: string;
	name: string;
	price: number;
	description: string;
	imageUrl: string;
}

export function FeaturedItemCard(product: Product) {
	return (
		<Card className="w-[300px] flex flex-col">
			<Link
				href={`/product/${product.id}`}
				className="flex-grow"
			>
				<CardContent className="pt-4">
					<div className="relative w-full h-[200px] mb-4">
						<Image
							src={product.imageUrl}
							alt={product.name}
							fill
							className="object-cover rounded-md"
						/>
					</div>
					<h3 className="font-semibold text-lg mb-2">{product.name}</h3>
					<p className="text-sm text-muted-foreground mb-2">
						{product.description}
					</p>
					<p className="text-lg font-bold">${product.price.toFixed(2)}</p>
				</CardContent>
			</Link>
			<CardFooter className="mt-auto">
				<Button className="w-full bg-[#59d473] hover:bg-[#429b58]">
					Add to Cart
				</Button>
			</CardFooter>
		</Card>
	);
}
