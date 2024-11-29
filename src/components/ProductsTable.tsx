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
	onDeleteProduct: (productId: number) => void;
}

export function ProductsTable({
	products,
	onEditProduct,
	onDeleteProduct,
}: ProductsTableProps) {
	return (
		<div className="overflow-x-auto">
			<table className="min-w-full border border-gray-200 dark:border-gray-700">
				<thead className="bg-gray-100 dark:bg-gray-800">
					<tr>
						<th className="py-2 px-4 border-b text-left text-gray-700 dark:text-gray-200">
							ID
						</th>
						<th className="py-2 px-4 border-b text-left text-gray-700 dark:text-gray-200">
							Name
						</th>
						<th className="py-2 px-4 border-b text-left text-gray-700 dark:text-gray-200">
							Price
						</th>
						<th className="py-2 px-4 border-b text-left text-gray-700 dark:text-gray-200">
							Category
						</th>
						<th className="py-2 px-4 border-b text-left text-gray-700 dark:text-gray-200">
							Stock
						</th>
						<th className="py-2 px-4 border-b text-left text-gray-700 dark:text-gray-200">
							Featured
						</th>
						<th className="py-2 px-4 border-b text-left text-gray-700 dark:text-gray-200">
							Created At
						</th>
						<th className="py-2 px-4 border-b text-left text-gray-700 dark:text-gray-200">
							Actions
						</th>
					</tr>
				</thead>
				<tbody>
					{products.map((product) => (
						<tr
							key={product.id}
							className="hover:bg-gray-50 dark:hover:bg-gray-700"
						>
							<td className="py-2 px-4 border-b text-gray-900 dark:text-gray-100">
								{product.id}
							</td>
							<td className="py-2 px-4 border-b text-gray-900 dark:text-gray-100">
								{product.name}
							</td>
							<td className="py-2 px-4 border-b text-gray-900 dark:text-gray-100">
								${product.price.toFixed(2)}
							</td>
							<td className="py-2 px-4 border-b text-gray-900 dark:text-gray-100">
								{product.category}
							</td>
							<td className="py-2 px-4 border-b text-gray-900 dark:text-gray-100">
								{product.stock}
							</td>
							<td className="py-2 px-4 border-b text-gray-900 dark:text-gray-100">
								{product.featured ? 'Yes' : 'No'}
							</td>
							<td className="py-2 px-4 border-b text-gray-900 dark:text-gray-100">
								{new Date(product.created_at).toLocaleDateString()}
							</td>
							<td className="py-2 px-4 border-b text-gray-900 dark:text-gray-100">
								<button
									onClick={() => onEditProduct(product.id)}
									className="text-blue-500 hover:underline mr-2"
								>
									Edit
								</button>
								<button
									onClick={() => onDeleteProduct(product.id)}
									className="text-red-500 hover:underline"
								>
									Delete
								</button>
							</td>
						</tr>
					))}
				</tbody>
			</table>
		</div>
	);
}
