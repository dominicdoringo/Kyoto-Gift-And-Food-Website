'use client';

import React, { useState, useEffect } from 'react';
import { ChevronLeft, ChevronRight } from 'lucide-react';
import { useRef } from 'react';
import { Button } from '@/components/ui/button';
import { FeaturedItemCard } from '@/components/ui/featured-item-card';
import { getProductById } from '@/api/api';
import { Product } from '@/lib/types';

const listItems = [
	{
		id: '0',
		name: 'Pocky Chocolate',
		price: 2.99,
		description: 'Classic Japanese chocolate-coated biscuit sticks',
		imageUrl: 'https://m.media-amazon.com/images/I/81UAcnIvi5L.jpg',
	},
	{
		id: '1',
		name: 'Matcha KitKat',
		price: 4.99,
		description: 'Green tea flavored chocolate wafer bars',
		imageUrl: 'https://m.media-amazon.com/images/I/81co+3MgqlL.jpg',
	},
	{
		id: '2',
		name: 'Ramune Soda',
		price: 2.49,
		description: 'Japanese marble soft drink with unique bottle design',
		imageUrl:
			'https://m.media-amazon.com/images/I/81fDajWWbkL._AC_UF894,1000_QL80_.jpg',
	},
	{
		id: '3',
		name: 'Mochi Ice Cream',
		price: 5.99,
		description: 'Sweet rice dough filled with ice cream',
		imageUrl: 'https://m.media-amazon.com/images/I/81ix0M-Bk3L.jpg',
	},
	{
		id: '4',
		name: 'Hawaiian Sun',
		price: 3.99,
		description: 'Passion fruit flavored tropical drink',
		imageUrl: 'https://m.media-amazon.com/images/I/81qnbcdAFoL.jpg',
	},
	{
		id: '5',
		name: 'Shin Instant Ramen',
		price: 1.99,
		description: 'Quick and delicious authentic Asian noodles',
		imageUrl: 'https://m.media-amazon.com/images/I/81kFdSChhKL.jpg',
	},
];

export function ListItems({ title = '' }) {
	const scrollContainerRef = useRef<HTMLDivElement>(null);

	const [products, setProducts] = useState<Product | null>(null);

	useEffect(() => {
		// Define an array of product IDs you want to fetch
		const productIds = ['1', '2', '3'];

		// Fetch product data
		const fetchProducts = async () => {
			const fetchedProducts: Product[] = [];
			for (let id of productIds) {
				const product = await getProductById(id);
				if (product != null) {
					fetchedProducts.push(product);
				}
			}
			setProducts(fetchedProducts);
		};

		fetchProducts();
	}, []);

	const scroll = (direction: 'left' | 'right') => {
		if (scrollContainerRef.current) {
			const scrollAmount = 330; // Card width + gap
			const scrollLeft = scrollContainerRef.current.scrollLeft;
			const newScrollLeft =
				direction === 'left'
					? scrollLeft - scrollAmount
					: scrollLeft + scrollAmount;

			scrollContainerRef.current.scrollTo({
				left: newScrollLeft,
				behavior: 'smooth',
			});
		}
	};

	return (
		<section className="py-12 px-6">
			<div className="max-w-7xl mx-auto">
				<h2 className="text-4xl font-bold text-center mb-8">{title}</h2>
				<div className="relative">
					<div
						ref={scrollContainerRef}
						className="flex gap-6 overflow-x-hidden scroll-smooth pb-4"
					>
						{products.map((item, index) => (
							<FeaturedItemCard
								key={index}
								{...item}
							/>
						))}
					</div>
					<Button
						variant="outline"
						size="icon"
						className="absolute left-0 top-1/2 -translate-y-1/2 -translate-x-4 bg-background shadow-lg"
						onClick={() => scroll('left')}
					>
						<ChevronLeft className="h-4 w-4" />
					</Button>
					<Button
						variant="outline"
						size="icon"
						className="absolute right-0 top-1/2 -translate-y-1/2 translate-x-4 bg-background shadow-lg"
						onClick={() => scroll('right')}
					>
						<ChevronRight className="h-4 w-4" />
					</Button>
				</div>
			</div>
		</section>
	);
}
