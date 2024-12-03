'use client';

import { ListItems } from '@/components/list-items';

export function Categories() {
	return (
		<main>
			<ListItems
				title={'Snacks'}
				categoryType={'snacks'}
			/>
			<ListItems
				title={'Drinks'}
				categoryType={'drinks'}
			/>
			<ListItems
				title={'Frozen'}
				categoryType={'frozen'}
			/>
			<ListItems
				title={'Sushi'}
				categoryType={'sushi'}
			/>
		</main>
	);
}
