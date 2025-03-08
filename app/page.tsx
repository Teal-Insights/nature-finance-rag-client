'use client';

import { useChat } from '@ai-sdk/react';

export default function Chat() {
  const { messages, input, handleInputChange, handleSubmit } = useChat({
    maxSteps: 3,
  });
  
  // Add debug logging when messages change
  console.log('Current messages:', messages);
  
  return (
    <div className="flex flex-col w-full max-w-md py-24 mx-auto stretch">
      <div className="space-y-4">
        {messages.map(m => (
          <div key={m.id} className="whitespace-pre-wrap">
            <div>
              <div className="font-bold">{m.role}</div>
              <p>
                {m.content.length > 0 ? (
                  m.content
                ) : (
                  <span className="italic font-light">
                    processing...
                  </span>
                )}
              </p>
              
              {m.parts?.map((part, index) => (
                part.type === 'tool-invocation' && part.toolInvocation && (
                  <div key={index} className="mt-2 p-2 bg-gray-100 rounded-md">
                    <p className="text-sm text-gray-700">
                      <span className="font-semibold">Tool call:</span> {String(part.toolInvocation.toolName)}
                    </p>
                    {part.toolInvocation.args && (
                      <p className="text-sm text-gray-600 mt-1">
                        <span className="font-semibold">Input:</span> {JSON.stringify(part.toolInvocation.args)}
                      </p>
                    )}
                    {part.toolInvocation.state === 'result' && (
                      <p className="text-sm text-gray-600 mt-1">
                        <span className="font-semibold">Result:</span> {JSON.stringify((part.toolInvocation as any).result)}
                      </p>
                    )}
                  </div>
                )
              ))}
            </div>
          </div>
        ))}
      </div>

      <form onSubmit={handleSubmit}>
        <input
          className="fixed bottom-0 w-full max-w-md p-2 mb-8 border border-gray-300 rounded shadow-xl"
          value={input}
          placeholder="Say something..."
          onChange={handleInputChange}
        />
      </form>
    </div>
  );
}