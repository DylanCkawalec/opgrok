import {
	IExecuteFunctions,
	INodeExecutionData,
	INodeType,
	INodeTypeDescription,
	NodeOperationError,
} from 'n8n-workflow';

export class GrokAiAssistant implements INodeType {
	description: INodeTypeDescription = {
		displayName: 'Grok AI Assistant',
		name: 'grokAiAssistant',
		icon: 'file:grok.svg',
		group: ['transform'],
		version: 1,
		subtitle: '={{$parameter["operation"] + ": " + $parameter["model"]}}',
		description: 'Interact with xAI Grok models directly in your workflows',
		defaults: {
			name: 'Grok AI',
		},
		inputs: ['main'],
		outputs: ['main'],
		credentials: [
			{
				name: 'grokApi',
				required: true,
			},
		],
		properties: [
			{
				displayName: 'Operation',
				name: 'operation',
				type: 'options',
				noDataExpression: true,
				options: [
					{
						name: 'Chat Completion',
						value: 'chat',
						description: 'Send a message and get AI response',
					},
					{
						name: 'Analyze Workflow',
						value: 'analyzeWorkflow',
						description: 'AI analyzes current workflow and suggests improvements',
					},
					{
						name: 'Generate Node Config',
						value: 'generateConfig',
						description: 'AI generates configuration for a specific node type',
					},
					{
						name: 'Enhance Data',
						value: 'enhanceData',
						description: 'AI enhances/transforms incoming data',
					},
				],
				default: 'chat',
			},
			// Chat operation fields
			{
				displayName: 'Model',
				name: 'model',
				type: 'options',
				options: [
					{
						name: 'Grok 4 (Latest)',
						value: 'grok-4-0709',
					},
					{
						name: 'Grok 4 Fast',
						value: 'grok-4-fast-non-reasoning',
					},
					{
						name: 'Grok 3 Mini (Fastest)',
						value: 'grok-3-mini',
					},
					{
						name: 'Grok Code Fast',
						value: 'grok-code-fast-1',
					},
				],
				default: 'grok-4-fast-non-reasoning',
				description: 'Which Grok model to use',
			},
			{
				displayName: 'Prompt',
				name: 'prompt',
				type: 'string',
				typeOptions: {
					rows: 4,
				},
				default: '',
				required: true,
				displayOptions: {
					show: {
						operation: ['chat', 'enhanceData', 'generateConfig'],
					},
				},
				description: 'The prompt to send to Grok',
				placeholder: 'Analyze this data and extract key insights...',
			},
			{
				displayName: 'System Prompt',
				name: 'systemPrompt',
				type: 'string',
				typeOptions: {
					rows: 2,
				},
				default: 'You are a helpful AI assistant embedded in an n8n workflow.',
				displayOptions: {
					show: {
						operation: ['chat'],
					},
				},
				description: 'System instructions for the AI',
			},
			{
				displayName: 'Include Input Data',
				name: 'includeInputData',
				type: 'boolean',
				default: true,
				description: 'Whether to include input data in the prompt context',
			},
			{
				displayName: 'Temperature',
				name: 'temperature',
				type: 'number',
				typeOptions: {
					minValue: 0,
					maxValue: 2,
					numberStepSize: 0.1,
				},
				default: 0.7,
				description: 'Creativity level (0 = focused, 2 = creative)',
			},
			{
				displayName: 'Max Tokens',
				name: 'maxTokens',
				type: 'number',
				typeOptions: {
					minValue: 1,
					maxValue: 4096,
				},
				default: 1024,
				description: 'Maximum length of response',
			},
		],
	};

	async execute(this: IExecuteFunctions): Promise<INodeExecutionData[][]> {
		const items = this.getInputData();
		const returnData: INodeExecutionData[] = [];
		
		const credentials = await this.getCredentials('grokApi');
		const apiKey = credentials.apiKey as string;
		const baseUrl = credentials.baseUrl as string || 'https://api.x.ai/v1';
		
		const operation = this.getNodeParameter('operation', 0) as string;

		for (let i = 0; i < items.length; i++) {
			try {
				const model = this.getNodeParameter('model', i) as string;
				const temperature = this.getNodeParameter('temperature', i) as number;
				const maxTokens = this.getNodeParameter('maxTokens', i) as number;
				const includeInputData = this.getNodeParameter('includeInputData', i) as boolean;

				let messages: Array<{role: string, content: string}> = [];

				if (operation === 'chat') {
					const systemPrompt = this.getNodeParameter('systemPrompt', i) as string;
					const userPrompt = this.getNodeParameter('prompt', i) as string;

					messages.push({
						role: 'system',
						content: systemPrompt,
					});

					// Include input data if requested
					let fullPrompt = userPrompt;
					if (includeInputData && items[i].json) {
						fullPrompt += '\n\nInput Data:\n' + JSON.stringify(items[i].json, null, 2);
					}

					messages.push({
						role: 'user',
						content: fullPrompt,
					});

				} else if (operation === 'analyzeWorkflow') {
					// Special operation: analyze the current workflow
					messages.push({
						role: 'system',
						content: 'You are an n8n workflow optimization expert. Analyze workflows and suggest improvements.',
					});
					messages.push({
						role: 'user',
						content: `Analyze this workflow data and suggest optimizations:\n${JSON.stringify(items[i].json, null, 2)}`,
					});

				} else if (operation === 'enhanceData') {
					const prompt = this.getNodeParameter('prompt', i) as string;
					messages.push({
						role: 'system',
						content: 'You are a data enhancement AI. Transform and enrich data as requested.',
					});
					messages.push({
						role: 'user',
						content: `${prompt}\n\nData to enhance:\n${JSON.stringify(items[i].json, null, 2)}`,
					});
				}

				// Call Grok API
				const response = await this.helpers.httpRequest({
					method: 'POST',
					url: `${baseUrl}/chat/completions`,
					headers: {
						'Authorization': `Bearer ${apiKey}`,
						'Content-Type': 'application/json',
					},
					body: {
						model,
						messages,
						temperature,
						max_tokens: maxTokens,
						stream: false,
					},
					json: true,
				});

				const content = response.choices[0]?.message?.content || '';
				const usage = response.usage || {};

				returnData.push({
					json: {
						response: content,
						model,
						usage: {
							promptTokens: usage.prompt_tokens || 0,
							completionTokens: usage.completion_tokens || 0,
							totalTokens: usage.total_tokens || 0,
						},
						metadata: {
							operation,
							timestamp: new Date().toISOString(),
						},
					},
					pairedItem: { item: i },
				});

			} catch (error) {
				if (this.continueOnFail()) {
					returnData.push({
						json: {
							error: error.message,
							operation,
						},
						pairedItem: { item: i },
					});
					continue;
				}
				throw new NodeOperationError(this.getNode(), error, { itemIndex: i });
			}
		}

		return [returnData];
	}
}
