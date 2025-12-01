import { GoogleGenerativeAI } from "@google/generative-ai";
import { NextResponse } from "next/server";

export async function POST(req: Request) {
    try {
        const { resumeLatex, jobDescription } = await req.json();

        if (!resumeLatex || !jobDescription) {
            return NextResponse.json(
                { error: "Missing resumeLatex or jobDescription" },
                { status: 400 }
            );
        }

        const apiKey = process.env.GEMINI_API_KEY;
        if (!apiKey) {
            return NextResponse.json(
                { error: "GEMINI_API_KEY is not set" },
                { status: 500 }
            );
        }

        const genAI = new GoogleGenerativeAI(apiKey);
        // Using gemini-2.0-flash as verified in the CLI
        const model = genAI.getGenerativeModel({ model: "gemini-2.0-flash" });

        const prompt = `
You are an expert resume consultant and LaTeX wizard.
Your task is to tailor the following LaTeX resume to better match the provided job description.
You should:
1. Analyze the job description for key skills, qualifications, and keywords.
2. Modify the resume content to highlight these relevant areas.
3. Adjust the summary/objective (if present) to align with the job role.
4. Rephrase bullet points to emphasize impact and relevance to the job.
5. MAINTAIN the exact LaTeX structure and formatting. Do not break the code.
6. Return ONLY the valid LaTeX code for the tailored resume. Do not include markdown code blocks (like \`\`\`latex ... \`\`\`), just the raw code.

Job Description:
${jobDescription}

Resume LaTeX:
${resumeLatex}
`;

        const result = await model.generateContent(prompt);
        const response = await result.response;
        let text = response.text();

        // Clean up markdown code blocks if present
        if (text.startsWith("\`\`\`latex")) {
            text = text.substring(8);
        } else if (text.startsWith("\`\`\`")) {
            text = text.substring(3);
        }
        if (text.endsWith("\`\`\`")) {
            text = text.substring(0, text.length - 3);
        }

        return NextResponse.json({ tailoredLatex: text.trim() });
    } catch (error) {
        console.error("Error tailoring resume:", error);
        return NextResponse.json(
            { error: "Failed to tailor resume" },
            { status: 500 }
        );
    }
}
