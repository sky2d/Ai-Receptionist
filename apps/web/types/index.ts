export interface Tenant {
    id: string;
    businessName: string;
}

export interface Conversation {
    id: string;
    tenantId: string;
    channel: 'phone' | 'sms' | 'web' | 'whatsapp';
    status: 'active' | 'completed' | 'escalated';
}

export interface Message {
    id: string;
    conversationId: string;
    sender: 'user' | 'agent' | 'system';
    content: string;
    timestamp: string;
}
