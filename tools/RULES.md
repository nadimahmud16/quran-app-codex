# Rules for daily English reading-practice summaries

Reader: a Bangla speaker improving his English reading, plus other Muslim readers of the same level. Each day's summary covers the ayahs read that day in a Quran-in-one-year plan, and gets a little harder as the year goes on.

## Content
- Base it ONLY on the English (Saheeh International) text printed by `show`. Never add stories, names, reasons, tafsir or details that are not in the text. No rulings, no opinions. Be respectful.
- Write "Allah", not "God" ("no god but Him" / "one God" are fine where the text says that).
- Summarize in your own words; do not copy long phrases.
- Split into paragraphs by topic: when the ayahs move to a different topic, start a new paragraph. Usually 1 to 4 paragraphs (5 max).
- Each paragraph has "ref" (the ayah range it covers) and "text". Ranges together must cover ALL the day's ayahs, in order, with no gaps or overlaps. Formats: "2:11-16", "2:20" (single ayah), or "2:284-3:5" for a range crossing into the next surah (better: split at the surah boundary into separate paragraphs, e.g. "2:284-286" and "3:1-15").
- Short "title", max 9 words.

## Difficulty (total words of all paragraphs together)
- Level 1, Days 1-60: 100-150 words. Very short sentences (under 12 words). Only common, simple words.
- Level 2, Days 61-120: 150-200 words. Short sentences, a few new words.
- Level 3, Days 121-180: 200-250 words. Mix of short and medium sentences.
- Level 4, Days 181-240: 250-300 words. Some longer sentences with words like "because", "although", "which".
- Level 5, Days 241-300: 300-350 words. Richer vocabulary, some linking phrases.
- Level 6, Days 301-365: 350-400 words. Natural, fluent English with varied sentences.
- If the day's ayahs are very short and few, it's fine to be a little under the range. Never go over the max.

## hardWords
The most useful harder words used in your summary (the exact form as used in the text): 4 words for Levels 1-2, 5 for Levels 3-4, 6 for Levels 5-6. Each {"w": word as used, "m": very simple English meaning, "bn": the Bangla meaning in Bangla script}. Avoid repeating the same hard words day after day; pick fresh ones when you can.

## File format
Write each day to `data/sum/day-N.json` (UTF-8, ensure_ascii False):
{"day": N, "level": L, "title": "...", "paragraphs": [{"ref": "...", "text": "..."}], "words": <total word count = sum of len(text.split())>, "hardWords": [{"w": "...", "m": "...", "bn": "..."}]}
Compute "words" with Python, don't guess.

## Example (Day 22, Level 1)
{"day":22,"level":1,"title":"Abraham, Honest Trust, and the Prophets' Promise","paragraphs":[{"ref":"3:67-68","text":"Abraham was not a Jew or a Christian. He turned to the truth. He was a Muslim who submitted to Allah. His true followers are closest to him. Allah is the protector of the believers."},{"ref":"3:69-74","text":"Some People of the Book want to mislead you. But they only mislead themselves. Why do they hide the truth they know? All bounty is in His hand. He gives it to whom He wills."},{"ref":"3:75-78","text":"Some of them return a large trust. Others will not return even one coin. Allah loves those who keep their promise and fear Him. Some sell Allah's covenant for a small price. Their punishment is painful."},{"ref":"3:79-83","text":"A prophet would never say, \"Worship me.\" Allah took a promise from the prophets. They must support a messenger who confirms their Book. All in the heavens and earth submit to Allah. All will return to Him."}],"words":143,"hardWords":[{"w":"mislead","m":"to lead someone the wrong way","bn":"বিপথে নেওয়া"},{"w":"bounty","m":"a big, kind gift","bn":"অনুগ্রহ / দান"},{"w":"covenant","m":"a serious promise","bn":"অঙ্গীকার / চুক্তি"},{"w":"submit","m":"to obey fully","bn":"আত্মসমর্পণ করা"}]}
