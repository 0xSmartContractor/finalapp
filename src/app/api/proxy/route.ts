import { NextResponse } from 'next/server';

export async function POST(req: Request) {
  try {
    const { prompt } = await req.json();
    
    // Call your Python backend
    const response = await fetch('http://your-python-server/generate', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        // Add any auth headers for your Python server
        'Authorization': `Bearer ${process.env.PYTHON_SERVER_SECRET}`
      },
      body: JSON.stringify({ prompt })
    });
    
    const data = await response.json();
    return NextResponse.json(data);
    
  } catch (error) {
    console.error('Error:', error);
    return NextResponse.json(
      { error: 'Failed to process request' },
      { status: 500 }
    );
  }
}