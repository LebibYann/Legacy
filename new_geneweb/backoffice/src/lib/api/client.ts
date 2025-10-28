import axios, { type AxiosInstance, type AxiosRequestConfig } from 'axios';
import type { components } from './schema';

/**
 * API Client for Geneweb Backend
 * Auto-generated wrapper based on OpenAPI schema
 */
export class GenewebApiClient {
	private client: AxiosInstance;

	constructor(baseURL: string = '/api', config?: AxiosRequestConfig) {
		this.client = axios.create({
			baseURL,
			headers: {
				'Content-Type': 'application/json'
			},
			...config
		});
	}

	// ===== Base Operations =====

	/**
	 * List all bases
	 * GET /api/bases
	 */
	async listBases(): Promise<components['schemas']['BaseListResponse']> {
		const response = await this.client.get<components['schemas']['BaseListResponse']>('/bases');
		return response.data;
	}

	/**
	 * Create a new base
	 * POST /api/bases
	 */
	async createBase(
		data: components['schemas']['BaseCreateRequest']
	): Promise<components['schemas']['BaseCreateResponse']> {
		const response = await this.client.post<components['schemas']['BaseCreateResponse']>(
			'/bases',
			data
		);
		return response.data;
	}

	/**
	 * Delete a base
	 * DELETE /api/bases/{base_name}
	 */
	async deleteBase(baseName: string): Promise<components['schemas']['BaseDeleteResponse']> {
		const response = await this.client.delete<components['schemas']['BaseDeleteResponse']>(
			`/bases/${baseName}`
		);
		return response.data;
	}

	// ===== Family Operations =====

	/**
	 * Create a family
	 * POST /api/bases/{base_id}/families
	 */
	async createFamily(
		baseId: number,
		data: components['schemas']['FamilyCreateRequest']
	): Promise<components['schemas']['FamilyCreateResponse']> {
		const response = await this.client.post<components['schemas']['FamilyCreateResponse']>(
			`/bases/${baseId}/families`,
			data
		);
		return response.data;
	}

	/**
	 * Create a family related to an individual
	 * POST /api/bases/{base_id}/families/to
	 */
	async createFamilyToIndividual(
		baseId: number,
		data: components['schemas']['FamilyCreateToIndividualRequest']
	): Promise<components['schemas']['FamilyCreateToIndividualResponse']> {
		const response = await this.client.post<
			components['schemas']['FamilyCreateToIndividualResponse']
		>(`/bases/${baseId}/families/to`, data);
		return response.data;
	}

	/**
	 * Get family details
	 * GET /api/bases/{base_id}/families/{family_id}
	 */
	async getFamily(
		baseId: number,
		familyId: number
	): Promise<components['schemas']['FamilyGetResponse']> {
		const response = await this.client.get<components['schemas']['FamilyGetResponse']>(
			`/bases/${baseId}/families/${familyId}`
		);
		return response.data;
	}

	/**
	 * Update a family
	 * PUT /api/bases/{base_id}/families/{family_id}
	 */
	async updateFamily(
		baseId: number,
		familyId: number,
		data: components['schemas']['FamilyUpdateRequest']
	): Promise<components['schemas']['FamilyUpdateResponse']> {
		const response = await this.client.put<components['schemas']['FamilyUpdateResponse']>(
			`/bases/${baseId}/families/${familyId}`,
			data
		);
		return response.data;
	}

	/**
	 * Delete a family
	 * DELETE /api/bases/{base_id}/families/{family_id}
	 */
	async deleteFamily(
		baseId: number,
		familyId: number
	): Promise<components['schemas']['FamilyDeleteResponse']> {
		const response = await this.client.delete<components['schemas']['FamilyDeleteResponse']>(
			`/bases/${baseId}/families/${familyId}`
		);
		return response.data;
	}

	/**
	 * Merge two families
	 * PATCH /api/bases/{base_id}/families/merge
	 */
	async mergeFamilies(
		baseId: number,
		data: components['schemas']['FamilyMergeRequest']
	): Promise<components['schemas']['FamilyMergeResponse']> {
		const response = await this.client.patch<components['schemas']['FamilyMergeResponse']>(
			`/bases/${baseId}/families/merge`,
			data
		);
		return response.data;
	}

	// ===== Individual Operations =====

	/**
	 * Create an individual
	 * POST /api/bases/{base_id}/individuals
	 */
	async createIndividual(
		baseId: number,
		data: components['schemas']['IndividualCreateRequest']
	): Promise<components['schemas']['IndividualCreateResponse']> {
		const response = await this.client.post<components['schemas']['IndividualCreateResponse']>(
			`/bases/${baseId}/individuals`,
			data
		);
		return response.data;
	}

	/**
	 * Get an individual
	 * GET /api/bases/{base_id}/individuals/{individual_id}
	 */
	async getIndividual(
		baseId: number,
		individualId: number
	): Promise<components['schemas']['IndividualGetResponse']> {
		const response = await this.client.get<components['schemas']['IndividualGetResponse']>(
			`/bases/${baseId}/individuals/${individualId}`
		);
		return response.data;
	}

	/**
	 * Delete an individual
	 * DELETE /api/bases/{base_id}/individuals/{individual_id}
	 */
	async deleteIndividual(
		baseId: number,
		individualId: number
	): Promise<components['schemas']['IndividualDeleteResponse']> {
		const response = await this.client.delete<components['schemas']['IndividualDeleteResponse']>(
			`/bases/${baseId}/individuals/${individualId}`
		);
		return response.data;
	}

	// ===== Utility Methods =====

	/**
	 * Set custom headers for all requests
	 */
	setHeaders(headers: Record<string, string>) {
		Object.assign(this.client.defaults.headers, headers);
	}

	/**
	 * Set authentication token (Bearer)
	 */
	setAuthToken(token: string) {
		this.client.defaults.headers.common['Authorization'] = `Bearer ${token}`;
	}

	/**
	 * Set Basic Authentication credentials
	 */
	setBasicAuth(username: string, password: string) {
		const encoded = btoa(`${username}:${password}`);
		this.client.defaults.headers.common['Authorization'] = `Basic ${encoded}`;
	}

	/**
	 * Remove authentication header
	 */
	clearAuth() {
		delete this.client.defaults.headers.common['Authorization'];
	}

	/**
	 * Get the underlying axios instance for advanced usage
	 */
	getAxiosInstance(): AxiosInstance {
		return this.client;
	}
}

// Export a default instance
export const apiClient = new GenewebApiClient();

// Export types for convenience
export type Base = components['schemas']['Base'];
export type BaseCreateRequest = components['schemas']['BaseCreateRequest'];
export type BaseCreateResponse = components['schemas']['BaseCreateResponse'];
export type BaseDeleteResponse = components['schemas']['BaseDeleteResponse'];
export type BaseListResponse = components['schemas']['BaseListResponse'];
export type FamilyCreateRequest = components['schemas']['FamilyCreateRequest'];
export type FamilyCreateResponse = components['schemas']['FamilyCreateResponse'];
export type FamilyCreateToIndividualRequest =
	components['schemas']['FamilyCreateToIndividualRequest'];
export type FamilyCreateToIndividualResponse =
	components['schemas']['FamilyCreateToIndividualResponse'];
export type FamilyDeleteResponse = components['schemas']['FamilyDeleteResponse'];
export type FamilyGetResponse = components['schemas']['FamilyGetResponse'];
export type FamilyMergeRequest = components['schemas']['FamilyMergeRequest'];
export type FamilyMergeResponse = components['schemas']['FamilyMergeResponse'];
export type FamilyUpdateRequest = components['schemas']['FamilyUpdateRequest'];
export type FamilyUpdateResponse = components['schemas']['FamilyUpdateResponse'];
export type GenderType = components['schemas']['GenderType'];
export type IndividualCreateRequest = components['schemas']['IndividualCreateRequest'];
export type IndividualCreateResponse = components['schemas']['IndividualCreateResponse'];
export type IndividualDeleteResponse = components['schemas']['IndividualDeleteResponse'];
export type IndividualGetResponse = components['schemas']['IndividualGetResponse'];
