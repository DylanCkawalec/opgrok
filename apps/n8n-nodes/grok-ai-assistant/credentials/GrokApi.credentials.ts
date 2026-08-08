import {
	ICredentialType,
	INodeProperties,
} from 'n8n-workflow';

export class GrokApi implements ICredentialType {
	name = 'grokApi';
	displayName = 'Grok AI API';
	documentationUrl = 'https://docs.x.ai';
	properties: INodeProperties[] = [
		{
			displayName: 'API Key',
			name: 'apiKey',
			type: 'string',
			typeOptions: {
				password: true,
			},
			default: '',
			required: true,
			description: 'Your xAI API key from https://console.x.ai',
		},
		{
			displayName: 'Base URL',
			name: 'baseUrl',
			type: 'string',
			default: 'https://api.x.ai/v1',
			description: 'Base URL for xAI API',
		},
	];
}
