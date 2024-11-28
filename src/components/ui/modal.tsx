// components/ui/modal.tsx
import React from 'react';
import { Button } from './button';

interface ModalProps {
	onClose: () => void;
	children: React.ReactNode;
}

export function Modal({ onClose, children }: ModalProps) {
	return (
		<div className="fixed inset-0 z-50 flex items-center justify-center bg-black bg-opacity-50">
			<div className="bg-white dark:bg-gray-800 text-black dark:text-white rounded-lg shadow-lg max-w-md w-full mx-4">
				<div className="p-6">{children}</div>
				<div className="flex justify-end p-4">
					<Button
						variant="ghost"
						onClick={onClose}
					>
						Close
					</Button>
				</div>
			</div>
		</div>
	);
}
