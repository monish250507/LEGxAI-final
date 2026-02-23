'use client';

import React, { useState, useEffect } from 'react';
import { useParams, useRouter } from 'next/navigation';
import RiskDistributionChart from '@/src/components/RiskDistributionChart';
import StrengthComparisonChart from '@/src/components/StrengthComparisonChart';

interface Clause {
  clause_id: string;
  text: string;
  type: string;
  priority_score: number;
  color: string;
  rank: number;
  explanation?: string;
  offensive_analysis?: string;
  defensive_analysis?: string;
  constitution_reference?: string;
  risk_level: 'high' | 'medium' | 'low' | 'unknown';
}

interface AnalysisData {
  status: string;
  filename: string;
  clauses: Clause[];
  document_text?: string;
  strategic_intelligence?: {
    case_summary: string;
    case_type: string;
    core_legal_issue: string;
    jurisdiction: string;
    primary_risk_domain: string;
    constitutional_articles_triggered: string[];
    risk_strength_index: number;
    risk_category: 'low' | 'moderate' | 'high';
    ai_confidence: number;
    risk_distribution: {
      high: number;
      medium: number;
      low: number;
    };
    strength_comparison: {
      offensive_strength: number;
      defensive_strength: number;
    };
    strategic_recommendations: string[];
  };
}

interface ChatMessage {
  id: string;
  text: string;
  sender: 'user' | 'ai';
  timestamp: Date;
}

export default function AnalysisPage() {
  const params = useParams();
  const router = useRouter();
  const documentId = params.id as string;
  
  const [analysisData, setAnalysisData] = useState<AnalysisData | null>(null);
  const [selectedClause, setSelectedClause] = useState<Clause | null>(null);
  const [isLoading, setIsLoading] = useState(true);
  const [chatOpen, setChatOpen] = useState(false);
  const [chatMessages, setChatMessages] = useState<ChatMessage[]>([]);
  const [chatInput, setChatInput] = useState('');

  useEffect(() => {
    const fetchAnalysis = async () => {
      try {
        // Mock API call - replace with actual backend integration
        // Generate different number of clauses based on document ID
        const isLargeDocument = documentId && documentId.includes('15') || Math.random() > 0.5;
        
        const baseClauses = [
          {
            clause_id: '1',
            text: 'The employee shall maintain confidentiality of all proprietary information and trade secrets.',
            type: 'confidentiality',
            priority_score: 9.2,
            color: '#ef4444',
            rank: 1,
            explanation: 'This clause establishes a legal obligation for employee to protect sensitive company information.',
            offensive_analysis: 'Can be used to enforce disciplinary action for breaches and potentially extend confidentiality obligations beyond employment termination.',
            defensive_analysis: 'Employee can challenge overly broad definitions of "proprietary information" and negotiate for clear limitations.',
            constitution_reference: 'Article 21: Protection of Life and Personal Liberty - Right to Privacy',
            risk_level: 'high'
          },
          {
            clause_id: '2',
            text: 'Either party may terminate this agreement with 30 days written notice.',
            type: 'termination',
            priority_score: 8.5,
            color: '#f59e0b',
            rank: 2,
            explanation: 'This clause provides both parties with the ability to end the employment relationship with reasonable notice period.',
            offensive_analysis: 'Employer can terminate employment quickly without cause, potentially leaving employee without immediate income.',
            defensive_analysis: 'Employee can ensure proper notice period and use termination as negotiation leverage for better severance.',
            constitution_reference: 'Article 19: Protection against arrest and detention - Right to livelihood',
            risk_level: 'medium'
          },
          {
            clause_id: '3',
            text: 'The company shall provide comprehensive health insurance coverage to all full-time employees.',
            type: 'benefits',
            priority_score: 7.8,
            color: '#00ff88',
            rank: 3,
            explanation: 'This clause establishes employer\'s commitment to provide healthcare benefits.',
            offensive_analysis: 'Employer can modify coverage levels or change insurance providers, potentially reducing benefits over time.',
            defensive_analysis: 'Employee can enforce minimum coverage standards and seek additional protections through regulatory compliance.',
            constitution_reference: 'Article 21: Right to Health and Environmental Protection',
            risk_level: 'low'
          },
          {
            clause_id: '4',
            text: 'Employee agrees to non-compete within 50 miles for 12 months after termination.',
            type: 'non-compete',
            priority_score: 8.9,
            color: '#ef4444',
            rank: 4,
            explanation: 'Restricts employee from working for competitors in specified geographic area and time period.',
            offensive_analysis: 'Severely limits employment opportunities and career advancement in employee\'s field and location.',
            defensive_analysis: 'Can challenge enforceability based on reasonableness of geographic scope and duration restrictions.',
            constitution_reference: 'Article 19: Right to practice any profession and to carry on any occupation',
            risk_level: 'high'
          },
          {
            clause_id: '5',
            text: 'All intellectual property created during employment belongs to the company.',
            type: 'intellectual_property',
            priority_score: 7.5,
            color: '#f59e0b',
            rank: 5,
            explanation: 'Assigns ownership rights of inventions, patents, and creative works to employer.',
            offensive_analysis: 'Company claims ownership of employee\'s innovations even those unrelated to job duties.',
            defensive_analysis: 'Employee can negotiate carve-outs for personal projects and prior inventions.',
            constitution_reference: 'Article 300A: Right to Property',
            risk_level: 'medium'
          },
          {
            clause_id: '6',
            text: 'Employee shall work 40 hours per week with overtime as required.',
            type: 'working_hours',
            priority_score: 6.8,
            color: '#00ff88',
            rank: 6,
            explanation: 'Defines standard work schedule and employer\'s right to require additional hours.',
            offensive_analysis: 'Employer can demand excessive overtime without adequate compensation or notice.',
            defensive_analysis: 'Employee entitled to overtime pay and can refuse unreasonable overtime requests.',
            constitution_reference: 'Article 42: Right to work and fair wages',
            risk_level: 'low'
          },
          {
            clause_id: '7',
            text: 'Company reserves right to modify policies and procedures at any time.',
            type: 'policy_modification',
            priority_score: 7.2,
            color: '#f59e0b',
            rank: 7,
            explanation: 'Gives employer unilateral authority to change workplace rules and regulations.',
            offensive_analysis: 'Employer can implement unfavorable policies without employee consent or negotiation.',
            defensive_analysis: 'Employee can challenge changes that violate labor laws or existing contractual obligations.',
            constitution_reference: 'Article 14: Equality before law',
            risk_level: 'medium'
          },
          {
            clause_id: '8',
            text: 'Disputes shall be resolved through arbitration rather than court proceedings.',
            type: 'dispute_resolution',
            priority_score: 8.1,
            color: '#f59e0b',
            rank: 8,
            explanation: 'Mandates alternative dispute resolution method outside traditional court system.',
            offensive_analysis: 'Limits employee\'s access to jury trial and public court proceedings, potentially favoring employer.',
            defensive_analysis: 'Can challenge arbitration clause if unconscionable or violates public policy.',
            constitution_reference: 'Article 21: Right to constitutional remedies',
            risk_level: 'medium'
          }
        ];

        // Additional clauses for larger documents (15 clauses total)
        const additionalClauses = [
          {
            clause_id: '9',
            text: 'Employee shall not solicit company clients or employees for 12 months post-termination.',
            type: 'non-solicitation',
            priority_score: 8.3,
            color: '#f59e0b',
            rank: 9,
            explanation: 'Prohibits employee from contacting company clients or poaching employees after leaving.',
            offensive_analysis: 'Restricts employee\'s ability to maintain professional relationships and start competing business.',
            defensive_analysis: 'Can challenge scope as overly broad and unreasonable restraint of trade.',
            constitution_reference: 'Article 19: Right to practice any profession',
            risk_level: 'medium'
          },
          {
            clause_id: '10',
            text: 'Company shall provide annual performance reviews and salary adjustments based on merit.',
            type: 'performance_review',
            priority_score: 6.5,
            color: '#00ff88',
            rank: 10,
            explanation: 'Establishes regular evaluation process and compensation adjustments.',
            offensive_analysis: 'Employer has discretion in performance evaluation and salary determination.',
            defensive_analysis: 'Employee can request objective criteria and appeal unfair evaluations.',
            constitution_reference: 'Article 14: Equality before law',
            risk_level: 'low'
          },
          {
            clause_id: '11',
            text: 'Employee must comply with all company policies and procedures as amended from time to time.',
            type: 'compliance',
            priority_score: 7.0,
            color: '#f59e0b',
            rank: 11,
            explanation: 'Requires adherence to current and future company regulations.',
            offensive_analysis: 'Employer can impose new obligations without employee consent.',
            defensive_analysis: 'Employee can challenge policies that violate legal rights or are unreasonable.',
            constitution_reference: 'Article 21: Right to life and personal liberty',
            risk_level: 'medium'
          },
          {
            clause_id: '12',
            text: 'Company shall provide paid time off accruing at 1.5 days per month of service.',
            type: 'leave_policy',
            priority_score: 6.2,
            color: '#00ff88',
            rank: 12,
            explanation: 'Defines paid leave accrual and usage entitlements.',
            offensive_analysis: 'Employer can restrict leave approval and modify accrual rates.',
            defensive_analysis: 'Employee entitled to earned leave and can challenge unreasonable denials.',
            constitution_reference: 'Article 21: Right to rest and leisure',
            risk_level: 'low'
          },
          {
            clause_id: '13',
            text: 'Employee agrees to indemnify company against any claims arising from employee actions.',
            type: 'indemnification',
            priority_score: 8.7,
            color: '#ef4444',
            rank: 13,
            explanation: 'Employee agrees to cover company losses from employee-related legal claims.',
            offensive_analysis: 'Places significant financial burden on employee for any work-related issues.',
            defensive_analysis: 'Can challenge scope and enforceability, especially for acts within scope of employment.',
            constitution_reference: 'Article 21: Right to equality before law',
            risk_level: 'high'
          },
          {
            clause_id: '14',
            text: 'Company may assign employee to different locations with reasonable notice.',
            type: 'relocation',
            priority_score: 7.4,
            color: '#f59e0b',
            rank: 14,
            explanation: 'Employer has right to transfer employee to different work locations.',
            offensive_analysis: 'Employer can force relocation disrupting employee\'s personal life and family.',
            defensive_analysis: 'Employee can negotiate relocation assistance and challenge unreasonable transfers.',
            constitution_reference: 'Article 19: Right to reside and settle in any part of India',
            risk_level: 'medium'
          },
          {
            clause_id: '15',
            text: 'This agreement constitutes the entire understanding between parties and supersedes prior agreements.',
            type: 'entire_agreement',
            priority_score: 6.8,
            color: '#00ff88',
            rank: 15,
            explanation: 'Contract represents complete agreement and replaces previous understandings.',
            offensive_analysis: 'Employer can claim verbal promises or side agreements are invalid.',
            defensive_analysis: 'Employee can challenge if fraud, misrepresentation, or ambiguity exists.',
            constitution_reference: 'Article 14: Equality before law',
            risk_level: 'low'
          }
        ];

        const allClauses = isLargeDocument ? [...baseClauses, ...additionalClauses] : baseClauses;

        const mockData: AnalysisData = {
          status: 'success',
          filename: isLargeDocument ? 'Service_Contract_15_Clauses.pdf' : 'Employment_Agreement_8_Clauses.pdf',
          clauses: allClauses,
          document_text: 'Full document text would appear here...',
          strategic_intelligence: {
            case_summary: `Mixed-risk case with ${allClauses.filter(c => c.risk_level === 'high').length} high-risk clauses among ${allClauses.length} total provisions requiring careful review.`,
            case_type: 'Employment Termination',
            core_legal_issue: 'Termination compliance and notice period requirements',
            jurisdiction: 'Multi-jurisdictional (US/International applicable)',
            primary_risk_domain: 'Employment Law',
            constitutional_articles_triggered: ['21', '19', '14'],
            risk_strength_index: 0.68,
            risk_category: 'moderate',
            ai_confidence: 0.85,
            risk_distribution: {
              high: allClauses.filter(c => c.risk_level === 'high').length,
              medium: allClauses.filter(c => c.risk_level === 'medium').length,
              low: allClauses.filter(c => c.risk_level === 'low').length
            },
            strength_comparison: {
              offensive_strength: 0.75,
              defensive_strength: 0.45
            },
            strategic_recommendations: [
              'Legal review recommended for moderate-risk provisions',
              'Request modifications to unclear or unfavorable terms',
              'Negotiate for more balanced risk allocation',
              'Ensure compliance with applicable labor laws',
              'Document any agreed modifications in writing',
              'Consider time limitations on restrictive clauses'
            ]
          }
        };
        setAnalysisData(mockData);
      } catch (error) {
        console.error('Failed to fetch analysis:', error);
      } finally {
        setIsLoading(false);
      }
    };

    if (documentId) {
      fetchAnalysis();
    }
  }, [documentId]);

  const getRiskColor = (risk: string) => {
    switch (risk) {
      case 'high': return '#ef4444';
      case 'medium': return '#f59e0b';
      case 'low': return '#10b981';
      default: return '#6b7280';
    }
  };

  const handleAskAI = (clause: Clause) => {
    // Open chatbot with pre-filled question about this clause
    setChatOpen(true);
    
    // Add a message about the clause
    const clauseMessage: ChatMessage = {
      id: Date.now().toString(),
      text: `Can you explain this clause in detail: "${clause.text}"? What are the legal implications?`,
      sender: 'user',
      timestamp: new Date()
    };
    
    setChatMessages([clauseMessage]);
    
    // Simulate AI response
    setTimeout(() => {
      const aiResponse: ChatMessage = {
        id: (Date.now() + 1).toString(),
        text: `This ${clause.type} clause has a **${clause.risk_level}** risk level with a priority score of ${clause.priority_score.toFixed(1)}/10.

**Legal Analysis:**
${clause.risk_level === 'high' ? 
  '⚠️ This clause contains potentially problematic language that could expose you to legal risks. I recommend careful review and possible negotiation.' :
  clause.risk_level === 'medium' ? 
  '🔍 This clause has some elements that warrant attention. Consider discussing with legal counsel.' :
  '✅ This clause appears to follow standard legal practices with minimal risk.'
}

**Key Points:**
- Clause Type: ${clause.type?.toUpperCase()}
- Risk Assessment: ${clause.risk_level?.toUpperCase()}
- Priority Score: ${clause.priority_score?.toFixed(1)}/10

Would you like me to suggest alternative wording or explain specific parts in more detail?`,
        sender: 'ai',
        timestamp: new Date()
      };
      
      setChatMessages(prev => [...prev, aiResponse]);
    }, 1000);
  };

  const handleDiscussWithExpert = (clause: Clause) => {
    // Simulate legal expert discussion
    const expertMessage = `
👨‍⚖️ Legal Expert Analysis for Clause #${clause.rank}

📋 **Clause Type**: ${clause.type?.toUpperCase()}
⚠️ **Risk Level**: ${clause.risk_level?.toUpperCase()}
🎯 **Priority Score**: ${clause.priority_score?.toFixed(1)}/10

💡 **Expert Recommendation**:
This clause appears to be ${clause.risk_level === 'high' ? 'potentially problematic' : clause.risk_level === 'medium' ? 'moderately concerning' : 'generally acceptable'} from a legal standpoint.

${clause.risk_level === 'high' ? 
  '⚠️ **Immediate Action Required**: We strongly recommend negotiating the terms of this clause to reduce legal exposure.' :
  clause.risk_level === 'medium' ? 
  '🔍 **Review Recommended**: Consider discussing this clause with legal counsel before signing.' :
  '✅ **Generally Acceptable**: This clause follows standard legal practices.'
}

📞 **Next Steps**: 
- Schedule a consultation with our legal team
- Request alternative clause wording
- Review similar clauses in your industry

Would you like to proceed with scheduling a consultation?
    `;
    
    alert(expertMessage);
  };

  const handleSendMessage = () => {
    if (!chatInput.trim()) return;

    const userMessage: ChatMessage = {
      id: Date.now().toString(),
      text: chatInput,
      sender: 'user',
      timestamp: new Date()
    };

    setChatMessages(prev => [...prev, userMessage]);
    setChatInput('');

    // Simulate AI response
    setTimeout(() => {
      const aiResponse: ChatMessage = {
        id: (Date.now() + 1).toString(),
        text: `I understand your question about "${chatInput.substring(0, 30)}...". 

Based on your question, let me provide a more detailed response:

**🤖 LexAI Legal Assistant Analysis:**

I can help you with:
- **Clause-specific analysis** - Select any clause and ask about its legal implications
- **Risk assessments** - High/Medium/Low risk evaluations with confidence scores
- **Negotiation strategies** - Specific suggestions to improve clause wording
- **Constitutional compliance** - Analysis against Indian Constitution articles
- **Legal enforceability** - Whether clauses can be legally enforced

**📋 Current Document Context:**
You have ${analysisData?.clauses.length || 0} clauses analyzed with confidence scores ranging from 6.2 to 9.2/10.

**🎯 To get better responses:**
1. Select a specific clause first
2. Ask direct questions like "Is this confidentiality clause enforceable?"
3. Request specific help like "How can I negotiate this non-compete?"

**💡 Try asking:**
- "What are the risks of the selected clause?"
- "Can you help me negotiate better terms?"
- "Is this clause constitutional under Article 19?"

Please select a clause or ask a more specific question!`,
        sender: 'ai',
        timestamp: new Date()
      };
      
      setChatMessages(prev => [...prev, aiResponse]);
    }, 1500);
  };

  const getRiskBgColor = (riskLevel: string) => {
    switch (riskLevel) {
      case 'high':
        return 'bg-red-900/20';
      case 'medium':
        return 'bg-yellow-900/20';
      case 'low':
        return 'bg-green-900/20';
      default:
        return 'bg-gray-900/20';
    }
  };

  const handleClauseClick = (clause: Clause) => {
    setSelectedClause(clause);
  };

  const handleDownload = () => {
    // Mock download - replace with actual API call
    alert('Download feature would call backend annotated document endpoint');
  };

  if (isLoading) {
    return (
      <div className="min-h-screen bg-black flex items-center justify-center">
        <div className="text-green-400 text-lg">Loading analysis...</div>
      </div>
    );
  }

  if (!analysisData) {
    return (
      <div className="min-h-screen bg-black flex items-center justify-center">
        <div className="text-red-400 text-lg">Analysis not found</div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-black">
      {/* Header */}
      <div className="border-b border-green-900 bg-black">
        <div className="px-6 py-4">
          <div className="flex items-center justify-between">
            <div className="flex items-center gap-3">
              <div className="w-8 h-8 bg-green-500 rounded-lg flex items-center justify-center">
                <span className="text-black font-bold text-sm">L</span>
              </div>
              <div>
                <h1 className="text-green-400 font-bold text-xl">Document Analysis</h1>
                <p className="text-gray-500 text-sm">{analysisData.filename}</p>
              </div>
            </div>
            <div className="flex items-center gap-4">
              <button 
                onClick={() => router.push('/dashboard')}
                className="bg-black border border-green-800 text-gray-400 px-4 py-2 rounded-lg hover:border-green-500 hover:text-green-400 transition-all duration-200"
              >
                ← Back to Dashboard
              </button>
              <button 
                onClick={handleDownload}
                className="bg-black border border-green-500 text-green-400 px-4 py-2 rounded-lg hover:bg-green-950 hover:text-green-300 hover:shadow-[0_0_15px_rgba(0,255,136,0.3)] transition-all duration-300"
              >
                📥 Download Annotated
              </button>
            </div>
          </div>
        </div>
      </div>

      {/* Two-Column Layout */}
      <div className="flex h-[calc(100vh-73px)]">
        {/* Left Side - Document Viewer */}
        <div className="w-1/2 border-r border-green-900 bg-gray-950 p-6 overflow-y-auto">
          <div className="mb-4">
            <h2 className="text-green-400 font-bold text-lg mb-4">Document Viewer</h2>
            
            {/* Strategic Intelligence Summary */}
          {analysisData.strategic_intelligence && (
            <div className="bg-black border border-green-800 rounded-lg p-6 mb-6">
              <div className="border-b border-green-700 pb-4 mb-4">
                <h2 className="text-green-400 font-bold text-xl mb-4">Strategic Intelligence Summary</h2>
                
                <div className="grid grid-cols-1 md:grid-cols-2 gap-6 mb-6">
                  {/* Case Overview */}
                  <div className="bg-gray-950 rounded-lg p-4 border border-green-800">
                    <h3 className="text-green-400 font-semibold text-lg mb-3">Case Overview</h3>
                    <div className="space-y-2">
                      <div className="flex justify-between items-center">
                        <span className="text-gray-400">Case Type:</span>
                        <span className="text-white font-medium">{analysisData.strategic_intelligence.case_type}</span>
                      </div>
                      <div className="flex justify-between items-center">
                        <span className="text-gray-400">Core Legal Issue:</span>
                        <span className="text-white font-medium">{analysisData.strategic_intelligence.core_legal_issue}</span>
                      </div>
                      <div className="flex justify-between items-center">
                        <span className="text-gray-400">Jurisdiction:</span>
                        <span className="text-white font-medium">{analysisData.strategic_intelligence.jurisdiction}</span>
                      </div>
                      <div className="flex justify-between items-center">
                        <span className="text-gray-400">Primary Risk Domain:</span>
                        <span className="text-white font-medium">{analysisData.strategic_intelligence.primary_risk_domain}</span>
                      </div>
                    </div>
                    
                    <div className="mt-4">
                      <h4 className="text-green-400 font-medium mb-2">Executive Summary</h4>
                      <p className="text-white text-sm leading-relaxed">{analysisData.strategic_intelligence.case_summary}</p>
                    </div>
                    
                    <div className="mt-4">
                      <h4 className="text-green-400 font-medium mb-2">Constitutional Articles Triggered</h4>
                      <div className="flex flex-wrap gap-2">
                        {analysisData.strategic_intelligence.constitutional_articles_triggered.map((article, index) => (
                          <span key={index} className="bg-green-950 text-green-400 px-2 py-1 rounded text-xs font-mono">
                            Article {article}
                          </span>
                        ))}
                      </div>
                    </div>
                  </div>
                  
                  {/* Risk Strength Index */}
                  <div className="bg-gray-950 rounded-lg p-4 border border-green-800">
                    <h3 className="text-green-400 font-semibold text-lg mb-3">Risk Strength Index</h3>
                    <div className="space-y-4">
                      <div className="flex justify-between items-center mb-4">
                        <span className="text-gray-400">Risk Strength Index:</span>
                        <div className="flex items-center">
                          <div className="text-3xl font-bold text-green-400">{(analysisData.strategic_intelligence.risk_strength_index * 100).toFixed(0)}%</div>
                          <div className="text-gray-500 text-sm ml-2">/ 100%</div>
                        </div>
                      </div>
                      
                      <div className="flex justify-between items-center mb-4">
                        <span className="text-gray-400">Risk Category:</span>
                        <div className={`px-3 py-1 rounded text-sm font-semibold ${
                          analysisData.strategic_intelligence.risk_category === 'high' ? 'bg-red-900' :
                          analysisData.strategic_intelligence.risk_category === 'moderate' ? 'bg-yellow-900' : 'bg-green-900'
                        }`}>
                          <span className="text-white">
                            {analysisData.strategic_intelligence.risk_category === 'high' ? 'High Exposure' :
                             analysisData.strategic_intelligence.risk_category === 'moderate' ? 'Moderate Exposure' : 'Low Exposure'}
                          </span>
                        </div>
                      </div>
                      
                      <div className="flex justify-between items-center mb-4">
                        <span className="text-gray-400">AI Confidence:</span>
                        <div className="flex items-center">
                          <div className="text-3xl font-bold text-green-400">{(analysisData.strategic_intelligence.ai_confidence * 100).toFixed(0)}%</div>
                          <div className="text-gray-500 text-sm ml-2">AI Confidence</div>
                        </div>
                      </div>
                      
                      {/* Progress Bar */}
                      <div className="w-full bg-gray-800 rounded-full h-3">
                        <div 
                          className="bg-gradient-to-r from-green-600 to-green-400 h-full rounded-full transition-all duration-500"
                          style={{ width: `${analysisData.strategic_intelligence.ai_confidence * 100}%` }}
                        ></div>
                      </div>
                    </div>
                  </div>
                </div>
              </div>
          )}

          {/* Document Content with Highlights */}
            <div className="bg-black border border-green-800 rounded-lg p-6">
              <div className="space-y-4">
                {analysisData.clauses.map((clause, index) => (
                  <div
                    key={clause.clause_id}
                    onClick={() => handleClauseClick(clause)}
                    className={`
                      p-4 rounded-lg border-2 cursor-pointer transition-all duration-200
                      ${selectedClause?.clause_id === clause.clause_id 
                        ? 'border-green-400 bg-green-950' 
                        : 'border-gray-700 hover:border-green-600 hover:bg-gray-900'
                      }
                    `}
                    style={{
                      borderLeftColor: clause.color,
                      borderLeftWidth: '4px'
                    }}
                  >
                    <div className="flex items-start justify-between mb-2">
                      <span className="text-green-400 text-xs font-mono bg-green-950 px-2 py-1 rounded">
                        {clause.type?.toUpperCase() || 'UNKNOWN'}
                      </span>
                      <div className="flex items-center gap-2">
                        <span className="text-gray-500 text-xs">#{clause.rank}</span>
                        <div 
                          className={`px-2 py-1 rounded text-xs font-semibold ${getRiskBgColor(clause.risk_level)}`}
                          style={{ color: getRiskColor(clause.risk_level) }}
                        >
                          {clause.risk_level?.toUpperCase() || 'UNKNOWN'}
                        </div>
                      </div>
                    </div>
                    <p className="text-white text-sm leading-relaxed">
                      {clause.text}
                    </p>
                  </div>
                ))}
              </div>
            </div>
          </div>
        </div>

        {/* Right Side - Clause Analysis Panel */}
        <div className="w-1/2 bg-black p-6 overflow-y-auto">
          <div className="mb-6">
            <h2 className="text-green-400 font-bold text-lg mb-4">Clause Analysis</h2>
            
            {selectedClause ? (
              <div className="bg-black border border-green-500 rounded-xl p-6 space-y-6 hover:shadow-[0_0_20px_rgba(0,255,136,0.2)] transition-all duration-300">
                {/* Clause Header */}
                <div className="border-b border-green-900 pb-4 mb-4">
                  <div className="flex items-center justify-between mb-2">
                    <span className="text-green-400 text-sm font-mono bg-green-950 px-2 py-1 rounded">
                      {selectedClause.type?.toUpperCase() || 'UNKNOWN'}
                    </span>
                    <div className="flex items-center gap-2">
                      <span className="text-gray-400 text-xs">
                        Priority: {selectedClause.priority_score?.toFixed(1) || '0.0'}
                      </span>
                      <div 
                        className={`px-2 py-1 rounded text-xs font-semibold ${getRiskBgColor(selectedClause.risk_level)}`}
                        style={{ color: getRiskColor(selectedClause.risk_level) }}
                      >
                        {selectedClause.risk_level?.toUpperCase() || 'UNKNOWN'}
                      </div>
                    </div>
                  </div>
                  
                  <h3 className="text-white font-semibold text-lg mb-3">Clause Text</h3>
                  <p className="text-gray-300 leading-relaxed">
                    {selectedClause.text}
                  </p>
                </div>

                {/* Constitution Reference */}
                {selectedClause.constitution_reference && (
                  <div className="bg-gray-900 border border-gray-700 rounded-lg p-4">
                    <h4 className="text-green-400 text-sm font-semibold mb-2">
                      📜 Constitution Reference
                    </h4>
                    <p className="text-green-300 text-sm font-mono">
                      {selectedClause.constitution_reference}
                    </p>
                  </div>
                )}

                {/* Explanation */}
                {selectedClause.explanation && (
                  <div>
                    <h4 className="text-green-400 text-sm font-semibold mb-2">
                      📋 Explanation
                    </h4>
                    <p className="text-gray-300 leading-relaxed text-sm">
                      {selectedClause.explanation}
                    </p>
                  </div>
                )}

                {/* Offensive Analysis */}
                {selectedClause.offensive_analysis && (
                  <div>
                    <h4 className="text-red-400 text-sm font-semibold mb-2">
                      ⚔️ Offensive Analysis
                    </h4>
                    <p className="text-gray-300 leading-relaxed text-sm">
                      {selectedClause.offensive_analysis}
                    </p>
                  </div>
                )}

                {/* Defensive Analysis */}
                {selectedClause.defensive_analysis && (
                  <div>
                    <h4 className="text-blue-400 text-sm font-semibold mb-2">
                      🛡️ Defensive Analysis
                    </h4>
                    <p className="text-gray-300 leading-relaxed text-sm">
                      {selectedClause.defensive_analysis}
                    </p>
                  </div>
                )}

                {/* Strategic Recommendations */}
                {analysisData.strategic_intelligence?.strategic_recommendations && (
                  <div>
                    <h4 className="text-green-400 font-medium mb-3">Strategic Recommendations</h4>
                    <div className="space-y-2">
                      {analysisData.strategic_intelligence?.strategic_recommendations.map((recommendation, index) => (
                        <div key={index} className="flex items-start gap-3 p-3 bg-gray-950 rounded-lg border border-green-800">
                          <span className="text-green-400 text-sm">●</span>
                          <span className="text-white text-sm">{recommendation}</span>
                        </div>
                      ))}
                    </div>
                  </div>
                )}

                {/* Visualization Panel */}
                {analysisData.strategic_intelligence && (
                  <div className="bg-black border border-green-800 rounded-lg p-6 mb-6">
                    <h3 className="text-green-400 font-semibold text-lg mb-4">Risk Visualization</h3>
                    
                    <div className="grid grid-cols-1 md:grid-cols-2 gap-6 mb-6">
                      {/* Risk Distribution Chart */}
                      <div className="bg-gray-950 rounded-lg p-4 border border-green-800">
                        <RiskDistributionChart data={analysisData.strategic_intelligence.risk_distribution} />
                      </div>
                      
                      {/* Strength Comparison Chart */}
                      <div className="bg-gray-950 rounded-lg p-4 border border-green-800">
                        <StrengthComparisonChart data={analysisData.strategic_intelligence.strength_comparison} />
                      </div>
                    </div>
                  </div>
                )}

                {/* Action Buttons */}
                <div className="flex gap-3 pt-4 border-t border-green-900">
                  <button 
                    onClick={() => handleAskAI(selectedClause)}
                    className="flex-1 bg-gray-800 border border-green-800 text-green-400 py-2 rounded-lg hover:bg-green-950 hover:border-green-500 transition-all duration-200"
                  >
                    🤖 Ask AI About This Clause
                  </button>
                  <button 
                    onClick={() => handleDiscussWithExpert(selectedClause)}
                    className="flex-1 bg-gray-800 border border-green-800 text-green-400 py-2 rounded-lg hover:bg-green-950 hover:border-green-500 transition-all duration-200"
                  >
                    💬 Discuss with Legal Expert
                  </button>
                </div>
              </div>
            ) : (
              <div className="text-center py-16">
                <div className="w-20 h-20 bg-gray-800 rounded-full flex items-center justify-center mx-auto mb-4">
                  <span className="text-gray-500 text-3xl">📄</span>
                </div>
                <h3 className="text-gray-400 text-lg font-semibold mb-2">Select a Clause</h3>
                <p className="text-gray-500 text-sm">Click on any clause in the document to view detailed analysis</p>
              </div>
            )}
          </div>
        </div>
      </div>

      {/* Floating Chatbot Button */}
      <button
        onClick={() => setChatOpen(!chatOpen)}
        className="fixed bottom-6 right-6 w-14 h-14 bg-green-500 border-2 border-green-400 rounded-full flex items-center justify-center hover:bg-green-400 hover:shadow-[0_0_25px_rgba(0,255,136,0.6)] transition-all duration-300 z-50"
      >
        <span className="text-black font-bold text-xl">💬</span>
      </button>

      {/* Chatbot Panel (Overlay) */}
      {chatOpen && (
        <div className="fixed inset-0 bg-black/80 backdrop-blur-sm z-50 flex items-center justify-center">
          <div className="bg-black border border-green-500 rounded-2xl w-full max-w-2xl mx-4 h-[600px] flex flex-col">
            {/* Chat Header */}
            <div className="border-b border-green-900 p-4 flex items-center justify-between">
              <h3 className="text-green-400 font-bold text-lg">AI Legal Assistant</h3>
              <button 
                onClick={() => setChatOpen(false)}
                className="text-gray-400 hover:text-green-400 transition-colors duration-200"
              >
                ✕
              </button>
            </div>
            
            {/* Chat Messages */}
            <div className="flex-1 p-4 overflow-y-auto">
              <div className="space-y-4">
                {chatMessages.length === 0 ? (
                  <div className="flex justify-start">
                    <div className="bg-gray-800 border border-green-800 rounded-lg p-3 max-w-[80%]">
                      <p className="text-white text-sm">Hello! I can help you understand any clause in your document. What would you like to know?</p>
                    </div>
                  </div>
                ) : (
                  chatMessages.map((message) => (
                    <div key={message.id} className={`flex ${message.sender === 'user' ? 'justify-end' : 'justify-start'}`}>
                      <div className={`${
                        message.sender === 'user' 
                          ? 'bg-green-600 text-black' 
                          : 'bg-gray-800 border border-green-800 text-white'
                      } rounded-lg p-3 max-w-[80%]`}>
                        <p className="text-sm whitespace-pre-line">{message.text}</p>
                        <p className="text-xs opacity-70 mt-1">
                          {message.timestamp.toLocaleTimeString()}
                        </p>
                      </div>
                    </div>
                  ))
                )}
              </div>
            </div>
            
            {/* Chat Input */}
            <div className="border-t border-green-900 p-4">
              <div className="flex gap-2">
                <input
                  type="text"
                  value={chatInput}
                  onChange={(e) => setChatInput(e.target.value)}
                  onKeyPress={(e) => e.key === 'Enter' && handleSendMessage()}
                  placeholder="Ask about any clause..."
                  className="flex-1 bg-black border border-green-800 rounded-lg px-4 py-3 text-white placeholder-gray-600 focus:outline-none focus:ring-2 focus:ring-green-500 focus:border-transparent"
                />
                <button 
                  onClick={handleSendMessage}
                  className="bg-green-500 text-black px-6 py-3 rounded-lg hover:bg-green-400 transition-colors duration-200"
                >
                  Send
                </button>
              </div>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}
