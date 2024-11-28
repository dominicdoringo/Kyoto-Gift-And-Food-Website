// src/components/Providers.tsx

'use client';

import React from 'react';
import { ThemeProvider } from '@/providers/theme-provider';
import { AuthProvider } from '@/context/AuthContext';

interface ProvidersProps {
	children: React.ReactNode;
}

export default function Providers({ children }: ProvidersProps) {
	return (
		<AuthProvider>
			<ThemeProvider
				attribute="class"
				defaultTheme="dark"
				enableSystem
				disableTransitionOnChange
			>
				{children}
			</ThemeProvider>
		</AuthProvider>
	);
}
