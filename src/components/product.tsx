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

interface ProductPageProps {
	product: Product;
}

async function fetchReader(id: number) {
	let reader;

	const fetcher = await getProductById(id);
	if (fetcher != null || fetcher != undefined) {
		reader = fetcher;
	} else {
		reader = {
			id,
			name: 'name',
			description: '',
			price: 0,
			category: 'misc',
			stock: 0,
			featured: false,
			created_at: new Date(),
			imageUrl:
				'https://m.media-amazon.com/images/I/91gJhDXaehL._AC_UF894,1000_QL80_.jpg',
		};
	}
	console.log(reader);
	return reader;
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

export default function ProductPage(id: { id: number }) {
	const { isLoggedIn } = useAuth();
	const { toast } = useToast();
	const router = useRouter();
	const [addingToCart, setAddingToCart] = useState(false);
	//const [selectedImage, setSelectedImage] = useState(0);
	const [quantity, setQuantity] = useState(0);

	const [reader, setProduct] = useState<Product>(defaultValue);
	const identity = id.id;

	useEffect(() => {
		const loadProduct = async () => {
			const product = await fetchReader(identity);
			console.log(product);
			setProduct(product);
		};
		loadProduct();
	}, [identity]);

	console.log(reader);
	if (reader == null || reader == undefined) {
		return <div>Oops, Product not found</div>;
	}
	//console.log(reader);
	//console.log(id.id);

	/*// Mock product data - in real app would come from API
  const product: ProductData = {
    id: '1',
    name: 'Safoco Rice Vermicelli',
    price: 6.85,
    originalPrice: 9.79,
    discount: 30,
    rating: 5,
    reviews: 34,
    unit: '2.00 lb/each',
    images: [
      '/placeholder.svg?height=600&width=600',
      '/placeholder.svg?height=600&width=600',
      '/placeholder.svg?height=600&width=600'
    ]
  }*/

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
		<div className="max-w-7xl mx-auto px-4 py-8 grid md:grid-cols-2 gap-8">
			{/* Product Images */}
			<div className="space-y-4">
				<div className="relative aspect-square">
					<Image
						//src={product.images[selectedImage]}
						src={reader.imageUrl}
						alt={reader.name}
						fill
						className="object-cover rounded-lg"
					/>
				</div>
				{/*<div className="flex gap-4">
					{product.images.map((image, index) => (
						<button
							key={index}
							onClick={() => setSelectedImage(index)}
							className={`relative aspect-square w-24 rounded-lg overflow-hidden border-2 ${
								selectedImage === index
									? 'border-primary'
									: 'border-transparent'
							}`}
						>
							<Image
								src={image}
								alt={`${product.name} view ${index + 1}`}
								fill
								className="object-cover"
							/>
						</button>
					))}
				</div>*/}
			</div>

			{/* Product Info */}
			<div className="space-y-6">
				<div className="flex items-start justify-between">
					<div>
						<h1 className="text-3xl font-bold">{reader.name}</h1>
						{/*<p className="text-muted-foreground">{reader.unit}</p>*/}
						<p className="text-muted-foreground">{reader.description}</p>
					</div>
					<Button
						variant="ghost"
						size="icon"
					>
						<Bookmark className="h-5 w-5" />
					</Button>
				</div>

				{/* Rating */}
				{/*<div className="flex items-center gap-2">
					{[...Array(5)].map((_, i) => (
						<Star
							key={i}
							className="w-5 h-5 fill-primary text-primary"
						/>
					))}
					<span className="text-muted-foreground ml-2">{product.reviews}</span>
				</div>*/}

				{/* Price */}
				<div className="flex items-center gap-4">
					<div className="text-3xl font-bold">${reader.price}</div>
					{/*<div className="text-muted-foreground line-through">
						${product.originalPrice.toFixed(2)}
					</div>
					<div className="bg-red-500 text-white px-2 py-1 rounded-md text-sm">
						Get {product.discount}% off
					</div>*/}
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
							onClick={() => setQuantity(Math.max(0, quantity - 1))}
						>
							<Minus className="h-4 w-4" />
						</Button>
						<input
							type="number"
							id="quantity"
							value={quantity}
							onChange={(e) =>
								setQuantity(Math.max(0, parseInt(e.target.value) || 0))
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
					disabled={quantity === 0}
				>
					Add to Cart
				</Button>

				{/* Social Share */}
				{/*<div className="flex items-center gap-4 pt-4">
					<Button
						variant="outline"
						size="icon"
					>
						<Facebook className="h-5 w-5" />
					</Button>
					<Button
						variant="outline"
						size="icon"
					>
						<Twitter className="h-5 w-5" />
					</Button>
					<Button
						variant="outline"
						size="icon"
					>
						<Instagram className="h-5 w-5" />
					</Button>
				</div>*/}
			</div>
		</div>
	);
}
