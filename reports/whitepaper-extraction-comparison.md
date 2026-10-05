# Whitepaper image extraction and comparison

The visible source is section 2, Transactions, on printed page 2 of the [Bitcoin whitepaper](https://bitcoin.org/bitcoin.pdf). The image places the final paragraph's beginning inside WELCOME TO THE, earlier paragraphs inside BRAVE NEW WORLD, and its closing continuation along the bottom border.

This is a manual provisional transcription from the supplied image. It is not a certified complete word for word extraction. Lowercase/uppercase forms, punctuation, some letters, and physical line breaks remain uncertain. The artwork runs text along curved letter strokes; wrapping that into ordinary prose necessarily changes its layout. No missing words have been silently restored from the reference.

Each numbered entry corresponds to one title letter. The text below preserves apparent spelling and the explicitly recorded word fragments. It is a reading along the letter strokes, not a facsimile of every physical line. [A?] and [which?] are uncertain readings; square bracket spans remain unreadable.

## Image transcription by displayed letter

```text
01 WELCOME W
In the mint based model,

02 WELCOME E
the mint was aware

03 WELCOME L
of all transac

04 WELCOME C
tions and decided

05 WELCOME O
which arrived first.

06 WELCOME M
To accomplish this without a trusted

07 WELCOME E
party, transac
tions must

08 TO T
be publicly an

09 TO O
nounced, and we

10 THE T
need a system

11 THE H
for participans

12 THE E
to agree on a single history of the order

13 BRAVE B
We define an electronic coin as a chain of digital signatures. Each owner transfers the coin

14 BRAVE R
to the next by digitally signing a hash of the previous transaction and the public key of the next owner and adding these to the end of the coin.

15 BRAVE A
A payee can verify the signatures to verify the chain of ownership. The problem

16 BRAVE V
of course is the payee can't verify that one of the owners did not double

17 BRAVE E
spend the coin. [A?]
common solution
is to introdue
cent
ral au
thority,
or mint, that
checks every
tran
sacti
on
for double spen
ding. After

18 NEW N
each transaction, the coin must be returned to the mint to

19 NEW E
issue a new coin, and only
coins issued
directly from
the
mint
are trusted
not to be
dou
dle-
spent. The
problem with

20 NEW W
this solution is that the fate of the entire money system depends on the company running

21 WORLD W
the mint, with every transaction having to go through them, just like a bank.

22 WORLD O
We need a way for the payee to know that the previous owners did not sing any earlier transactions.

23 WORLD R
For our purposes, the earliest transaction is the one that counts, so we

24 WORLD L
don't care about later attempts to double-spend.

25 WORLD D
The only way to confirm the abcense of a transaction is to be aware of all transactions.

FOOTER
in [which?] they were recived the payee needs proof that at the time of each transaction the [partly obscured] of nodes agreed it was [obscured]
```

## Differences from the reference

| Location | Visible artwork | Reference | Assessment |
| --- | --- | --- | --- |
| BRAVE E | introdue | introduce | Apparent missing c; legible in enlarged crop |
| BRAVE E | No visible words between introdue and cent / ral | a trusted | Apparent omission; initial A before common remains uncertain |
| NEW E | dou / dle- / spent | double-spent | Apparent b to d substitution; split strokes make confidence lower |
| WORLD O | sing | sign | Apparent transposition of the last two letters |
| WORLD D | abcense | absence | Apparent s to c substitution |
| THE H | participans | participants | Apparent missing t; handwritten join is ambiguous |
| Footer | recived | received | Apparent missing e; partly crossed by frame |
| WELCOME TO | No visible citation marker after announced | [1] | Reference citation marker is not visibly reproduced |
| Footer tail | Several words crossed by black frame | See section 2 closing sentence | Not transcribed from reference; remains obscured |

## Reading order and limits

The artwork's displayed order starts with a later part of the whitepaper. To compare source order, read BRAVE NEW WORLD first, then WELCOME TO THE, then the footer. This reordering is an explicit comparison step; it does not alter the saved image transcription.

Word fragments can be joined for searching the reference, but their original splits remain in the letter records. In particular, joining the apparent dou/dle gives doudle, not double. The reference citation marker [1] after announced is not visible in the artwork.

The footer's tail is under the black border. Its expected wording is recoverable from the reference, but that would be reconstruction, not image extraction. The saved transcription therefore retains unreadable spans. The apparent word before they is also marked uncertain rather than asserted to match the reference.

The CSV lists observed differences rather than repeating the complete external whitepaper. Use the linked PDF for an authoritative view of the full original section. The JSON retains the supplied image hash, exact saved strings, uncertainty labels, reading order and explicit word joining operations.

## Every word alignment

[Open the complete word alignment CSV](whitepaper-every-word-alignment.csv). Every matched image token has its source position recorded. Differences are grouped into insertions or replacements; they are flagged for review, not silently corrected. The reference contains 286 tokens under the documented tokenizer; the provisional image reading has 282 after explicit fragment joins. Of those, 270 align as equal after ignoring case. These counts describe this transcription and tokenizer, not measured OCR accuracy or a hidden message. The raw letter records retain spelling, fragment splits and uncertain readings.
