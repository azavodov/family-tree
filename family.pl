child(A, B) :- parent(B, A).
father(A, B) :- parent(A, B), male(A).
mother(A, B) :- parent(A, B), female(A).
brother(A, B) :- sibling(A, B), male(A).
sister(A, B) :- sibling(A, B), female(A).
son(A, B) :- child(A, B), male(A).
daughter(A, B) :- child(A, B), female(A).
spouse(A, B) :- marriage(A, B, DM), DM < current_year, not((divorce(A, B, DD) , DD > DM)).
grandmother(A, B) :- mother(A, C), parent(C, B).
grandfather(A, B) :- father(A, C), parent(C, B).
grandchild(A, B) :- child(A, C), parent(B, C).
aunt(A, B) :- sister(A, P), parent(P, B).
uncle(A, B) :- brother(A, P), parent(P, B).
sibling(A, B) :- mother(M, A), father(F, A), mother(M, B), father(F, B), A \= B.
cousin(A, B) :- child(A, C), child(B, D), sibling(C, D).


is_alive(X, Date) :- birth(X, Born_Date), Date>Born_Date,
    (death(X, Death_Date), Date<Death_Date; not(death(X, _))).
is_dead(X, Date) :- not(is_alive(X, Date)).

child(A, B, Date) :- child(A, B), is_alive(A, Date).
parent(A, B, Date) :- parent(A, B), is_alive(B, Date).
father(A, B, Date) :- parent(A, B, Date), male(A).
mother(A, B, Date) :- parent(A, B, Date), female(A).
sibling(A, B, Date) :- mother(M, A, Date), father(F, A, Date), mother(M, B, Date), father(F, B, Date), A \= B.
brother(A, B, Date) :- sibling(A, B, Date), male(A).
sister(A, B, Date) :- sibling(A, B, Date), female(A).
son(A, B, Date) :- child(A, B, Date), male(A).
daughter(A, B, Date) :- child(A, B, Date), female(A).
spouse(A, B, Date) :- marriage(A, B, DM), DM =< Date, not((divorce(A, B, DD), DM =< DD, DD =< Date)).
grandmother(A, B, Date) :- mother(A, C, Date), parent(C, B, Date).
grandfather(A, B, Date) :- father(A, C, Date), parent(C, B, Date).
grandchild(A, B, Date) :- child(A, C, Date), parent(B, C, Date).
aunt(A, B, Date) :- sister(A, P, Date), parent(P, B, Date).
uncle(A, B, Date) :- brother(A, P, Date), parent(P, B, Date).
cousin(A, B, Date) :- child(A, C, Date), child(B, D, Date), sibling(C, D, Date).

marrige_date(A, B, Date) :- marriage(A, B, Date); marriage(B, A, Date).
divorce_date(A, B, Date) :- divorce(A, B, Date) ; divorce(B, A, Date).

single(Who, From, Until) :- birth(Who, From), (
      marrige_date(Who, _, Until), !; death(Who, Until), !; current_year(Until)
).

married(Who, From, Until) :- marrige_date(Who, Partner, From), (
      (death(Who, Until), is_alive(Partner, Until)), !;
      (death(Partner, Until), is_alive(Who, Until)), !;
      divorce_date(Who, Partner, Until), ! ; current_year(Until)
).

divorced(Who, From, Until) :- divorce_date(Who, _, From), (
      death(Who, Until), ! ;
      (marrige_date(Who, _, DM), DM > From) -> Until = DM, ! ;
      current_year(Until)
).

widowed(Who, From, Until) :- marrige_date(Who, Partner, DM),
      death(Partner, From), not((divorce_date(Who, Partner, DD), DD > DM)), From > DM, (
    		death(Who, Until), !;
            (marrige_date(Who, _, DM), DM > From) -> Until = DM, !;
            current_year(Until)
),  Until > From.
