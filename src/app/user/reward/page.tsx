// src/app/user/reward/page.tsx

'use client';

import React, { useState, useEffect } from 'react';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Badge } from '@/components/ui/badge';
import { API_HOST_BASE_URL } from '@/lib/constants';
import { useAuth } from '@/context/AuthContext';
import { useToast } from '@/hooks/use-toast';
import { useRouter } from 'next/navigation';
import { Button } from '@/components/ui/button'; // Optional: For retry or other actions

interface RewardData {
	points: number;
	reward_tier: string;
}

export default function RewardPage() {
	const { isLoggedIn, logout } = useAuth();
	const { toast } = useToast();
	const router = useRouter();

	const [rewardData, setRewardData] = useState<RewardData | null>(null);
	const [loading, setLoading] = useState<boolean>(true);
	const [error, setError] = useState<string | null>(null);

	// Retrieve accessToken from localStorage
	const accessToken =
		typeof window !== 'undefined' ? localStorage.getItem('accessToken') : null;

	useEffect(() => {
		if (!isLoggedIn || !accessToken) {
			toast({
				title: 'Not Authenticated',
				description: 'Please sign in to view your rewards.',
				variant: 'destructive',
			});
			router.push('/sign-in');
			return;
		}

		const fetchRewardData = async () => {
			try {
				const response = await fetch(`${API_HOST_BASE_URL}/rewards/`, {
					method: 'GET',
					headers: {
						'Content-Type': 'application/json',
						Authorization: `Bearer ${accessToken}`,
					},
				});

				if (response.ok) {
					const data = await response.json();
					setRewardData({
						points: data.points,
						reward_tier: data.reward_tier,
					});
				} else if (response.status === 404) {
					setError('Rewards not found. Please enroll in the rewards program.');
				} else if (response.status === 401) {
					setError('Unauthorized access. Please log in again.');
					logout();
					router.push('/sign-in');
				} else {
					const errorData = await response.json();
					setError(errorData.detail || 'Failed to fetch reward data.');
				}
			} catch (err) {
				console.error('Error fetching reward data:', err);
				setError('An unexpected error occurred while fetching reward data.');
			} finally {
				setLoading(false);
			}
		};

		fetchRewardData();
	}, [isLoggedIn, accessToken, router, toast, logout]);

	// Optional: Retry fetching data
	const handleRetry = () => {
		setLoading(true);
		setError(null);
		setRewardData(null);
		// Re-trigger useEffect by updating state or using a key
		// For simplicity, we can refactor fetchRewardData into a separate function
		// Here, we'll call fetchRewardData again
		(async () => {
			try {
				const response = await fetch(`${API_HOST_BASE_URL}/rewards/`, {
					method: 'GET',
					headers: {
						'Content-Type': 'application/json',
						Authorization: `Bearer ${accessToken}`,
					},
				});

				if (response.ok) {
					const data = await response.json();
					setRewardData({
						points: data.points,
						reward_tier: data.reward_tier,
					});
				} else if (response.status === 404) {
					setError('Rewards not found. Please enroll in the rewards program.');
				} else if (response.status === 401) {
					setError('Unauthorized access. Please log in again.');
					logout();
					router.push('/sign-in');
				} else {
					const errorData = await response.json();
					setError(errorData.detail || 'Failed to fetch reward data.');
				}
			} catch (err) {
				console.error('Error fetching reward data:', err);
				setError('An unexpected error occurred while fetching reward data.');
			} finally {
				setLoading(false);
			}
		})();
	};

	if (loading) {
		return (
			<div className="min-h-screen bg-white dark:bg-gray-900 flex items-center justify-center p-4">
				<p className="text-gray-700 dark:text-gray-300">
					Loading your rewards...
				</p>
			</div>
		);
	}

	if (error) {
		return (
			<div className="min-h-screen bg-white dark:bg-gray-900 flex items-center justify-center p-4">
				<div className="max-w-md w-full bg-white dark:bg-gray-800 shadow-lg rounded-lg p-6">
					<h2 className="text-2xl font-bold text-red-600 dark:text-red-400 mb-4">
						Error
					</h2>
					<p className="text-gray-700 dark:text-gray-300 mb-4">{error}</p>
					{error !== 'Unauthorized access. Please log in again.' && (
						<Button
							onClick={handleRetry}
							variant="outline"
						>
							Retry
						</Button>
					)}
				</div>
			</div>
		);
	}

	return (
		<div className="min-h-screen bg-white dark:bg-gray-900 flex items-center justify-center p-4">
			<Card className="w-full max-w-md bg-white dark:bg-gray-800 shadow-lg rounded-lg overflow-hidden">
				<CardHeader className="bg-green-600 dark:bg-green-700 text-white text-center py-6">
					<CardTitle className="text-2xl font-bold">Your Rewards</CardTitle>
				</CardHeader>
				<CardContent className="p-6">
					<div className="text-center">
						<h2 className="text-4xl font-bold text-gray-800 dark:text-white mb-2">
							{rewardData?.points}
						</h2>
						<p className="text-gray-600 dark:text-gray-300 mb-6">
							Reward Points
						</p>
						<Badge
							variant="outline"
							className={`px-4 py-2 text-lg font-semibold border-2 ${
								rewardData?.reward_tier === 'Gold'
									? 'border-yellow-500 text-yellow-500 dark:border-yellow-400 dark:text-yellow-400'
									: rewardData?.reward_tier === 'Silver'
										? 'border-gray-500 text-gray-500 dark:border-gray-400 dark:text-gray-400'
										: 'border-blue-500 text-blue-500 dark:border-blue-400 dark:text-blue-400'
							}`}
						>
							{rewardData?.reward_tier} Member
						</Badge>
					</div>
					<div className="mt-8 bg-green-50 dark:bg-green-900 rounded-lg p-4 border border-green-200 dark:border-green-700">
						<h3 className="text-lg font-semibold text-green-800 dark:text-green-200 mb-2">
							Membership Benefits:
						</h3>
						<ul className="list-disc list-inside text-gray-700 dark:text-gray-300 space-y-1">
							<li>Exclusive discounts on select items</li>
							<li>Early access to new product launches</li>
							<li>Birthday rewards</li>
							<li>Personalized offers based on your shopping habits</li>
						</ul>
					</div>
				</CardContent>
			</Card>
		</div>
	);
}
