'use client';

import { FeaturedItems } from '@/components/featured-items';
import { PromoBanner } from '@/components/promo-banner';

export default function Home() {
	return (
		<main>
			<FeaturedItems />
			<PromoBanner />
		</main>
	);
}
