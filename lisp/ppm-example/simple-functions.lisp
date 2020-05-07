
(defun gimme-ten () 
"A function that gives you 10."
  10
)

; Testing gimme-ten.
(format t "Results of calling 'gimme-ten':~%")
(format t "~D ~%~%" (gimme-ten))

(defun add-two (x y)
"A function that adds two numbers together."
  (+ x y)
)

; Testing add-two.
(format t "Results of calling 'add-two' on 1 and 3:~%")
(format t "~D ~%~%" (add-two 1 3))


(defun double-numbers (numbers) 
"A function that doubles all numbers in a list, returning
a new list."
  (loop for n in numbers
    collect (* n 2)
  )
)
; Testing double-numbers.
(defvar numbers '(1 2 3 4 5)) ; Our list of numbers.

(format t "Results of calling 'double-numbers' on ~S:~%" numbers)
(format t "~D ~%~%" (double-numbers numbers))
