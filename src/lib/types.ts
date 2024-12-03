type tokenResponse = {
	access_token: string;
	token_type: string;
};

export interface Product {
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
