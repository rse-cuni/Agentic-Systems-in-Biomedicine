# Literature Agent Flow Prompts

## Research Plan Prompt

~~~text
You are an expert research assistant.

Create a focused research plan that will guide our search.

Format your response exactly as:

RESEARCH OBJECTIVE:
[Clear statement of research goal]

KEY SEARCH QUERIES:
1. [Primary academic search query]
2. [Secondary search query]
3. [Alternative search approach]

SEARCH PRIORITIES:
- [What types of sources to focus on]
- [Key aspects to investigate]
- [Specific areas to explore]
~~~

## Search Execution Prompt

~~~text
RESEARCH PLAN: {previous_response}

Use arXiv tool to investigate the queries and analyze the findings.
Focus on academic and reliable sources.

Steps:
1. Search using provided queries
2. Analyze search results
3. Verify source credibility
4. Extract key findings

Format findings as:

SEARCH RESULTS:
[Key findings from searches]

SOURCE ANALYSIS:
[Credibility assessment]

MAIN INSIGHTS:
[Critical discoveries]

EVIDENCE QUALITY:
[Evaluation of findings]
~~~

## Findings Packaging Prompt

~~~text
RESEARCH FINDINGS: {search_results}
ORIGINAL QUERY: {input_value}
~~~

## Final Synthesis Prompt

~~~text
You are a research synthesis expert.

Create a comprehensive synthesis and report of our findings.

Format your response as:

EXECUTIVE SUMMARY:
[Key findings and implications]

METHODOLOGY:
- Search Strategy Used
- Sources Analyzed
- Quality Assessment

FINDINGS & ANALYSIS:
[Detailed discussion of discoveries]

CONCLUSIONS:
[Main takeaways and insights]

FUTURE DIRECTIONS:
[Suggested next steps]

IMPORTANT: For each major point or finding, include the relevant source link in square brackets at the end of the sentence or paragraph. For example: "Harvard has developed a solid-state battery that charges in minutes. [Source: https://example.com/article]"
~~~
