'use client';

import { useState } from 'react';
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
import api from '@/api/api';

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

interface Product {
	id: string;
	name: string;
	description: string;
	price: number;
	category: string;
	stock: number;
	featured: boolean;
	created_at: Date;
	imageUrl: string;
}

interface ProductPageProps {
	product: ProductData;
}

export default function ProductPage({ product }: ProductPageProps) {
	const [selectedImage, setSelectedImage] = useState(0);
	const [quantity, setQuantity] = useState(0);

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
		try {
			await api.post('/api/cart', {
				productId: product.id,
				quantity,
			});
			// Handle success - show toast, update cart count, etc.
		} catch (error) {
			// Handle error
			console.error('Error adding to cart:', error);
		}
	};

	return (
		<div className="max-w-7xl mx-auto px-4 py-8 grid md:grid-cols-2 gap-8">
			{/* Product Images */}
			<div className="space-y-4">
				<div className="relative aspect-square">
					<Image
						src={product.images[selectedImage]}
						alt={product.name}
						fill
						className="object-cover rounded-lg"
					/>
				</div>
				<div className="flex gap-4">
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
				</div>
			</div>

			{/* Product Info */}
			<div className="space-y-6">
				<div className="flex items-start justify-between">
					<div>
						<h1 className="text-3xl font-bold">{product.name}</h1>
						<p className="text-muted-foreground">{product.unit}</p>
					</div>
					<Button
						variant="ghost"
						size="icon"
					>
						<Bookmark className="h-5 w-5" />
					</Button>
				</div>

				{/* Rating */}
				<div className="flex items-center gap-2">
					{[...Array(5)].map((_, i) => (
						<Star
							key={i}
							className="w-5 h-5 fill-primary text-primary"
						/>
					))}
					<span className="text-muted-foreground ml-2">{product.reviews}</span>
				</div>

				{/* Price */}
				<div className="flex items-center gap-4">
					<div className="text-3xl font-bold">${product.price.toFixed(2)}</div>
					<div className="text-muted-foreground line-through">
						${product.originalPrice.toFixed(2)}
					</div>
					<div className="bg-red-500 text-white px-2 py-1 rounded-md text-sm">
						Get {product.discount}% off
					</div>
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
				<div className="flex items-center gap-4 pt-4">
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
				</div>
			</div>
		</div>
	);
}
