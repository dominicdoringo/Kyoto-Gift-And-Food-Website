'use client';

import { useEffect, useState } from 'react';
import Image from 'next/image';
import {
	Star,
	Bookmark,
	Facebook,
	Twitter,
	Instagram,
	Minus,
	Plus,
} from 'lucide-react';
import { Button } from '@/components/ui/button';
import api, { getProductById } from '@/api/api';
import { Product } from '@/lib/types';
import { API_HOST_BASE_URL } from '@/lib/constants';
import { useRouter } from 'next/navigation';
import { useAuth } from '@/context/AuthContext';
import { useToast } from '@/hooks/use-toast';

interface ProductPageProps {
	id: number;
}

interface ProductData {
	id: string;
	name: string;
	price: number;
	originalPrice: number;
	discount: number;
	rating: number;
	reviews: number;
	unit: string;
	images: string[];
}

const defaultValue: Product = {
	id: 0,
	name: 'Oops, Product not Found!',
	description: 'The product you were looking for does not exist',
	price: 0,
	category: 'error',
	stock: 0,
	featured: false,
	created_at: new Date(),
	imageUrl:
		'https://m.media-amazon.com/images/I/91gJhDXaehL._AC_UF894,1000_QL80_.jpg',
};

// Utility function to extract error messages
const extractErrorMessage = (errorData: any): string => {
	if (typeof errorData.detail === 'string') {
		return errorData.detail;
	} else if (Array.isArray(errorData.detail)) {
		// If detail is an array, concatenate messages
		return errorData.detail.map((err: any) => err.msg).join(', ');
	} else if (typeof errorData.detail === 'object') {
		// If detail is an object, extract relevant messages
		return errorData.detail.msg || 'Failed to add item to cart.';
	}
	return 'Failed to add item to cart.';
};

async function fetchReader(id: number): Promise<Product> {
	try {
		const fetcher = await getProductById(id);
		if (fetcher) {
			return fetcher;
		} else {
			return defaultValue;
		}
	} catch (error) {
		console.error('Error fetching product:', error);
		return defaultValue;
	}
}

export default function ProductPage({ id }: ProductPageProps) {
	const { isLoggedIn } = useAuth();
	const { toast } = useToast();
	const router = useRouter();
	const [addingToCart, setAddingToCart] = useState(false);
	const [quantity, setQuantity] = useState(1);

	const [reader, setProduct] = useState<Product>(defaultValue);
	const identity = id;

	useEffect(() => {
		const loadProduct = async () => {
			const product = await fetchReader(identity);
			console.log(product);
			setProduct(product);
		};
		loadProduct();
	}, [identity]);

	console.log(reader);
	if (!reader || reader.category === 'error') {
		return <div>Oops, Product not found</div>;
	}

	const handleAddToCart = async () => {
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
					product_id: reader.id,
					quantity: quantity,
				}),
			});

			if (response.ok) {
				toast({
					title: 'Added to Cart',
					description: `${reader.name} has been added to your cart.`,
					variant: 'default',
				});
			} else {
				const errorData = await response.json();
				const errorMessage = extractErrorMessage(errorData);
				toast({
					title: 'Error',
					description: errorMessage,
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
		<div className="max-w-7xl mx-auto px-4 py-8 grid md:grid-cols-2 gap-8">
			{/* Product Images */}
			<div className="space-y-4">
				<div className="relative aspect-square">
					<Image
						src={reader.imageUrl}
						alt={reader.name}
						fill
						className="object-cover rounded-lg"
					/>
				</div>
				{/* Additional Images can be handled here */}
			</div>

			{/* Product Info */}
			<div className="space-y-6">
				<div className="flex items-start justify-between">
					<div>
						<h1 className="text-3xl font-bold">{reader.name}</h1>
						<p className="text-muted-foreground">{reader.description}</p>
					</div>
					<Button
						variant="ghost"
						size="icon"
					>
						<Bookmark className="h-5 w-5" />
					</Button>
				</div>

				{/* Price */}
				<div className="flex items-center gap-4">
					<div className="text-3xl font-bold">${reader.price}</div>
					{/* Original price and discount can be handled here */}
				</div>

				{/* Quantity Selector */}
				<div className="space-y-2">
					<label
						htmlFor="quantity"
						className="block text-sm font-medium"
					>
						Quantity
					</label>
					<div className="flex items-center gap-4">
						<Button
							variant="outline"
							size="icon"
							onClick={() => setQuantity(Math.max(1, quantity - 1))}
						>
							<Minus className="h-4 w-4" />
						</Button>
						<input
							type="number"
							id="quantity"
							value={quantity}
							onChange={(e) =>
								setQuantity(Math.max(1, parseInt(e.target.value) || 1))
							}
							className="w-20 text-center border rounded-md p-2"
						/>
						<Button
							variant="outline"
							size="icon"
							onClick={() => setQuantity(quantity + 1)}
						>
							<Plus className="h-4 w-4" />
						</Button>
					</div>
				</div>

				{/* Add to Cart Button */}
				<Button
					className="w-full"
					size="lg"
					onClick={handleAddToCart}
					disabled={quantity < 1 || addingToCart}
				>
					{addingToCart ? 'Adding...' : 'Add to Cart'}
				</Button>
			</div>
		</div>
	);
}
