'use client';

import { ListItems } from '@/components/list-items';

export function Categories() {
	return (
		<main>
			<ListItems title={'Snacks'} />
			<ListItems title={'Drinks'} />
			<ListItems title={'Frozen'} />
			<ListItems title={'Misc'} />
		</main>
	);
}
