Rapid Data Entry
By Alexandre Kaiser

Data Entry for not quantified data (such as physical items) can be cumbersome because the data is text and you usually would like accompanying images of the items.

This program takes a narrated video of a series of "show and tells" and uses that information to populate a ready-made database for the user.

1. Record video
2. Get transcript (whisper)
3. Timestamp the beginnings and end of each show and tell (!!! really difficult)
4. Take the respective portions of the transcript to populate a JSON object to store relevant information (LLM prompt)
5. Add a series of photos of the item to add to the database (use frames within timestamps)

Future tasks:
1. Before populating database, identify common class structures to store them similarly so that it is easier to query later
2. Identify the item in frame and add bounding box (or segment it out)
3. Extract relevant data from visual information
4. Run in realtime
5. Provide feedback (asking clarifying questions to have less null data columns)
6. Video-to-3D when relevant


For breaking things into facts, we handle facts one sentence at a time. This creates a few issues:
1. deictic expressions: context dependent words such as pronouns and other terms
2. general context: a scene has a time and place, but it wont be referred to in every sentence
3. multiple names: each subject might be referred to in multiple different ways

To handle deictic expressions we use a semantic checker to identify what the expression refers to explicitly. In the case of multiple names, attempt to link subjects that are likely to be identical just under different names.
