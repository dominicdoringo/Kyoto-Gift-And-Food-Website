// src/components/UsersTable.tsx

'use client';

import React from 'react';

interface User {
	id: number;
	username: string;
	email: string;
	is_admin: boolean;
	created_at: string;
}

interface UsersTableProps {
	users: User[];
	onEditUser: (userId: number) => void;
}

export function UsersTable({ users, onEditUser }: UsersTableProps) {
	return (
		<div className="overflow-x-auto">
			<table className="min-w-full border border-gray-200 dark:border-gray-700">
				<thead className="bg-gray-100 dark:bg-gray-800">
					<tr>
						<th className="py-2 px-4 border-b border-gray-200 dark:border-gray-700 text-left text-gray-700 dark:text-gray-200">
							ID
						</th>
						<th className="py-2 px-4 border-b border-gray-200 dark:border-gray-700 text-left text-gray-700 dark:text-gray-200">
							Username
						</th>
						<th className="py-2 px-4 border-b border-gray-200 dark:border-gray-700 text-left text-gray-700 dark:text-gray-200">
							Email
						</th>
						<th className="py-2 px-4 border-b border-gray-200 dark:border-gray-700 text-left text-gray-700 dark:text-gray-200">
							Admin
						</th>
						<th className="py-2 px-4 border-b border-gray-200 dark:border-gray-700 text-left text-gray-700 dark:text-gray-200">
							Created At
						</th>
						<th className="py-2 px-4 border-b border-gray-200 dark:border-gray-700 text-left text-gray-700 dark:text-gray-200">
							Actions
						</th>
					</tr>
				</thead>
				<tbody>
					{users.map((user) => (
						<tr
							key={user.id}
							className="hover:bg-gray-50 dark:hover:bg-gray-700"
						>
							<td className="py-2 px-4 border-b border-gray-200 dark:border-gray-700 text-gray-900 dark:text-gray-100">
								{user.id}
							</td>
							<td className="py-2 px-4 border-b border-gray-200 dark:border-gray-700 text-gray-900 dark:text-gray-100">
								{user.username}
							</td>
							<td className="py-2 px-4 border-b border-gray-200 dark:border-gray-700 text-gray-900 dark:text-gray-100">
								{user.email}
							</td>
							<td className="py-2 px-4 border-b border-gray-200 dark:border-gray-700 text-gray-900 dark:text-gray-100">
								{user.is_admin ? 'Yes' : 'No'}
							</td>
							<td className="py-2 px-4 border-b border-gray-200 dark:border-gray-700 text-gray-900 dark:text-gray-100">
								{new Date(user.created_at).toLocaleDateString()}
							</td>
							<td className="py-2 px-4 border-b border-gray-200 dark:border-gray-700 text-gray-900 dark:text-gray-100">
								<button
									onClick={() => {
										console.log('Editing user with ID:', user.id);
										onEditUser(user.id);
									}}
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
