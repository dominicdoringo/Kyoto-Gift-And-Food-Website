import React, { useState } from 'react';
import { useRouter } from 'next/navigation';
import { useAuth } from '@/context/AuthContext';
import { useToast } from '@/hooks/use-toast';
import { API_HOST_BASE_URL } from '@/lib/constants';
import { Product } from '@/lib/types';
import Link from 'next/link';

interface FeaturedItemCardProps {
	id: number;
	name: string;
	price: number;
	description?: string;
	imageUrl?: string;
	category?: string;
	stock?: number;
	featured?: boolean;
	created_at?: Date;
}

export function FeaturedItemCard({
	id,
	name,
	price,
	description = 'No description available.',
	imageUrl = '/default-image.png',
	stock = 0,
}: FeaturedItemCardProps): JSX.Element {
	const { isLoggedIn } = useAuth();
	const { toast } = useToast();
	const router = useRouter();
	const [addingToCart, setAddingToCart] = useState(false);

	const handleAddToCart = async (e: React.MouseEvent<HTMLButtonElement>) => {
		e.preventDefault(); // Prevent default button behavior
		e.stopPropagation(); // Prevent event from bubbling up to parent elements

		if (!isLoggedIn) {
			toast({
				title: 'Please Sign In',
				description: 'You need to be signed in to add items to your cart.',
				variant: 'destructive',
			});
			router.push('/sign-in');
			return;
		}

		const token = localStorage.getItem('accessToken');
		if (!token) {
			toast({
				title: 'Error',
				description: 'Authentication token not found.',
				variant: 'destructive',
			});
			router.push('/sign-in');
			return;
		}

		setAddingToCart(true);

		try {
			const response = await fetch(`${API_HOST_BASE_URL}/cart/`, {
				method: 'POST',
				headers: {
					'Content-Type': 'application/json',
					Authorization: `Bearer ${token}`,
				},
				body: JSON.stringify({
					product_id: id,
					quantity: 1, // default quantity
				}),
			});

			if (response.ok) {
				toast({
					title: 'Added to Cart',
					description: `${name} has been added to your cart.`,
					variant: 'default',
				});
			} else {
				const errorData = await response.json();
				toast({
					title: 'Error',
					description: errorData.detail || 'Failed to add item to cart.',
					variant: 'destructive',
				});
			}
		} catch (error) {
			console.error('Error adding to cart:', error);
			toast({
				title: 'Error',
				description: 'An unexpected error occurred.',
				variant: 'destructive',
			});
		} finally {
			setAddingToCart(false);
		}
	};

	return (
		<div className="w-72 sm:w-80 md:w-96 bg-white dark:bg-gray-800 shadow-md rounded-lg overflow-hidden flex flex-col">
			{/* Link wraps only the image and product info */}
			<Link
				href={`/product/${id}`}
				className="flex-grow"
			>
				<img
					src={imageUrl}
					alt={name}
					className="w-full h-48 object-cover"
				/>
				<div className="flex flex-col flex-1 p-4">
					<h3 className="text-xl font-semibold text-gray-900 dark:text-gray-100">
						{name}
					</h3>
					<p className="text-gray-600 dark:text-gray-300 flex-1 mt-2 line-clamp-3">
						{description}
					</p>
				</div>
			</Link>
			<div className="px-4 py-2 flex flex-col">
				<span className="text-lg font-bold text-gray-900 dark:text-gray-100">
					${price.toFixed(2)}
				</span>
				{/* Add to Cart button is outside the Link */}
				<button
					onClick={handleAddToCart}
					disabled={addingToCart || stock == 0}
					className={`mt-4 w-full px-4 py-2 bg-green-600 text-white rounded-md hover:bg-green-700 transition-colors duration-200 ${
						addingToCart || stock == 0 ? 'opacity-50 cursor-not-allowed' : ''
					}`}
				>
					{stock > 0
						? addingToCart
							? 'Adding...'
							: 'Add to Cart'
						: 'Out of Stock'}
				</button>
			</div>
		</div>
	);
}
