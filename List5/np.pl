#!/usr/bin/env swipl
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% Dictionary
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%


:- [skladnicaTagsBases].

hasTag(Word, Tag) :- tagAndBase(Word,_Base,Tag).

hasTag(w, prep:loc).

:- op(1050, xfx, ==>).

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% GRAMMAR
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%


likeAdj(adj:L:P:R:_, L, P, R).
likeAdj(ppas:L:P:R:_, L, P, R).

np(L,P,R) ==> adj(L,P,R), np(L,P,R).
np(L,P,R) ==> adv, adj(L,P,R), np(L,P,R).
np(L,P,R) ==> np(L,P,R), adj(L,P,R).
np(L,P,R) ==> np(L,P,R), adv, adj(L,P,R).
np(L,P,R) ==> np(L,P,R), np(_,gen,_).
np(L,P,R) ==> np(L,P,R), prep(P2), np(_, P2, _).

np(pl,P,R1) ==> np(_,P,R1), [i], np(_,P,_R2).
%np(pl,P,R1) ==> np(_,P,R1), conj, np(_,P,_R2).
%np(pl,P,R1) ==> np(_,P,R1), interp, np(_,P,_R2).
np(L,P,R)   ==> [X], {hasTag(X,subst:L:P:R)}.

adj(L,P,R)  ==> [X], {hasTag(X, Tag), likeAdj(Tag,L,P,R)}.
adv         ==> [X], {hasTag(X, adv:_)}.
prep(P)     ==> [X], {hasTag(X, prep:P)}.

%conj        ==> [X], {hasTag(X, conj), X \= 'to'}.
%interp     ==> [X], {hasTag(X, interp)}.


%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% Parse
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
commasToList((X,Y), [X|Rest]) :-
   !, commasToList(Y,Rest).
commasToList(X,[X]).


allign( [[W]| Rest], [W|T], Alligment) :-
   !,allign(Rest, T, Alligment).
allign( [At|Rest], Ts, [ (At,Pref) | ARest]):-
   Pref = [_|_],
   append(Pref, RestT, Ts),
   allign(Rest, RestT, ARest).
allign( [{C}], [], []) :- C.
allign( [], [], []).



parse(A,TokensToParse) :-
   (A ==> Right),
   commasToList(Right, ListRight),
   allign(ListRight, TokensToParse, Alligment),
   parsePairs(Alligment).

parsePairs([]).
parsePairs([(A,L)| Rest]):-
   parse(A,L),
   parsePairs(Rest).

writeList([A]) :- write(A),!.
writeList([A|As]):- write(A), write(' '),writeList(As).

parse0 :-
%   see('bad_phrases.pl'),
   see('phrases.pl'),
   parsing,
   seen.

parsing :-
   repeat,
   read(L),
   analyze(L),
   L = end_of_file,!.

analyze(L) :-
   length(L,N),
   N < 7,
   parse(np(_,_,_), L),
   write('GOOD:'),
   writeList(L),nl,!.
analyze(L) :-
   write('BAD:'), writeList(L),nl,!.


:- parse0.
:- halt.
