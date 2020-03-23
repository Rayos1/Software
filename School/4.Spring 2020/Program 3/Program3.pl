:- use_module(library(clpfd)).

write_to_file(File, Text) :-
    open(File, write, Stream),
    write(Stream, Text), nl,
    close(Stream).

students(0, []) :- !.
students(N, [(_Student,_Car,_Drink,_Sport,_Music)|T]) :- N1 is N-1, students(N1,T).

student(1, [H|_], H) :- !.
student(N, [_|T], R) :- N1 is N-1, student(N1, T, R).

% The accounting major lives in the first room
hint1(Students) :- student(1, Students, (accounting,_,_,_,_)).

% The computer science student lives in the middle of the corridor
hint2(Students) :- student(3, Students, (computer_science,_,_,_,_)).

% The history major is a jazz fan
hint3([(history,_,_,_,jazz)|_]).
hint3([_|T]) :- hint3(T).

% The Yankees fan drives a Toyota
hint4([(_,_,tea,yankees,_)|_]).
hint4([_|T]) :- hint4(T).

% The accounting major drinks Coke
hint5([(accounting,_,coke,_,_)|_]).
hint5([_|T]) :- hint5(T).

% The engineering major drinks coffee
hint6([(engineering,_,coffee,_,_)|_]).
hint6([_|T]) :- hint6(T).

% The computer science student and history student are neighbors
hint7([(computer_science,_,_,_,_),(history,_,_,_,_)|_]).
hint7([(history,_,_,_,_),(computer_science,_,_,_,_)|_]).
hint7([_|T]) :- hint7(T).

% The student at the far end of the hall likes classical music
hint8(Students) :- student(5, Students, (_,_,_,_,classical)).

% The tea drinker drives a Tesla
hint9([(_,tesla,tea,_,_)|_]).
hint9([_|T]) :- hint9(T).

% The classical music fan lives next to the jazz listener
hint10([(_,_,_,_,jazz),(_,_,_,_,classical)|_]).
hint10([(_,_,_,_,classical),(_,_,_,_,jazz)|_]).
hint10([_|T]) :- hint10(T).

% The English major does not live in either of the first two rooms
hint11(Students) :- student(3, Students, (english,_,_,_,_)).
hint11(Students) :- student(4, Students, (english,_,_,_,_)).
hint11(Students) :- student(5, Students, (english,_,_,_,_)).

% The Royals fan drives a Tesla
hint12([(_,tesla,_,royals,_)|_]).
hint12([_|T]) :- hint12(T).

% The Cubs fan listens to jazz
hint13([(_,_,_,cubs,jazz)|_]).
hint13([_|T]) :- hint13(T).

% The engineering major fllows the Chiefs
hint14([(engineering,_,_,chiefs,_)|_]).
hint14([_|T]) :- hint14(T).

% The first room is the home of the Broncos fan
hint15(Students) :- student(1, Students, (_,_,_,broncos,_)).

% The Coke drinker drives a Nissan
hint16([(_,nissan,coke,_,_)|_]).
hint16([_|T]) :- hint16(T).

% The country music fan and the techno fan are neighbors
hint17([(_,_,_,_,techno),(_,_,_,_,country)|_]).
hint17([(_,_,_,_,country),(_,_,_,_,techno)|_]).
hint17([_|T]) :- hint17(T).

% The fans of the 2 Kansas City teams (Chiefs and Royals) are neighbors
hint18([(_,_,_,chiefs,_),(_,_,_,royals,_)|_]).
hint18([(_,_,_,royals,_),(_,_,_,chiefs,_)|_]).
hint18([_|T]) :- hint18(T).

% The accounting major listens to rock music
hint19([(accounting,_,_,_,rock)|_]).
hint19([_|T]) :- hint19(T).

% The Yankees fan drinks milk
hint20([(_,_,milk,yankees,_)|_]).
hint20([_|T]) :- hint20(T).

% The Chevy driver listens to country music
hint21([(_,chevy,_,_,country)|_]).
hint21([_|T]) :- hint21(T).

% The jazz fan drives a Ford
hint22([(_,ford,_,_,jazz)|_]).
hint22([_|T]) :- hint22(T).

% What music does the computer-science student listen to, and what does the English major drink?
question([(computer_science,_,_,_,_)|_]).
question([_|T]) :- question(T).

solution(Students) :-
  students(5, Students),
  hint1(Students),
  hint2(Students),
  hint3(Students),
  hint4(Students),
  hint5(Students),
  hint6(Students),
  hint7(Students),
  hint8(Students),
  hint9(Students),
  hint10(Students),
  hint11(Students),
  hint12(Students),
  hint13(Students),
  hint14(Students),
  hint15(Students),
  hint16(Students),
  hint17(Students),
  hint18(Students),
  hint19(Students),
  hint20(Students),
  hint21(Students),
  hint22(Students),
  question(Students).


