// src/components/ProductsTable.tsx

'use client';

import React from 'react';

interface Product {
	id: number;
	name: string;
	description?: string;
	price: number;
	category: string;
	stock: number;
	featured: boolean;
	created_at: string;
}

interface ProductsTableProps {
	products: Product[];
	onEditProduct: (productId: number) => void;
}

export function ProductsTable({ products, onEditProduct }: ProductsTableProps) {
	return (
		<div className="overflow-x-auto">
			<table className="min-w-full border border-gray-200 dark:border-gray-700">
				<thead className="bg-gray-100 dark:bg-gray-800">
					<tr>
						<th className="py-2 px-4 border-b">ID</th>
						<th className="py-2 px-4 border-b">Name</th>
						<th className="py-2 px-4 border-b">Price</th>
						<th className="py-2 px-4 border-b">Category</th>
						<th className="py-2 px-4 border-b">Stock</th>
						<th className="py-2 px-4 border-b">Featured</th>
						<th className="py-2 px-4 border-b">Created At</th>
						<th className="py-2 px-4 border-b">Actions</th>
					</tr>
				</thead>
				<tbody>
					{products.map((product) => (
						<tr
							key={product.id}
							className="hover:bg-gray-50 dark:hover:bg-gray-700"
						>
							<td className="py-2 px-4 border-b">{product.id}</td>
							<td className="py-2 px-4 border-b">{product.name}</td>
							<td className="py-2 px-4 border-b">
								${product.price.toFixed(2)}
							</td>
							<td className="py-2 px-4 border-b">{product.category}</td>
							<td className="py-2 px-4 border-b">{product.stock}</td>
							<td className="py-2 px-4 border-b">
								{product.featured ? 'Yes' : 'No'}
							</td>
							<td className="py-2 px-4 border-b">
								{new Date(product.created_at).toLocaleDateString()}
							</td>
							<td className="py-2 px-4 border-b">
								<button
									onClick={() => onEditProduct(product.id)}
									className="text-blue-500 hover:underline"
								>
									Edit
								</button>
							</td>
						</tr>
					))}
				</tbody>
			</table>
		</div>
	);
}
