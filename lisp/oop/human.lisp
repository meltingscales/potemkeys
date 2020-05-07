(defclass Person ()
  (
    (name       
      :initarg :name
      :initform "Joe Schmoe"
      :type string)
    
    (happiness  
      :initarg :happiness
      :initform 100
      :type integer)

    (energy
      :initarg :energy
      :initform 100
      :type integer)
  )
)

(defmethod go-to-sleep ((p Person))
  (setf (slot-value p 'energy) 100) ;Why is energy not set to 100 here?!
  (format t "~S falls asleep. zzz..." (slot-value p 'name))
)


;(defclass OfficeWorker (Person)
;  (
;
;  )
;)

(defvar henry (make-instance 'Person :name "Henry"  :energy 0))
;(setf (slot-value henry 'energy) 100) ; Why does setf work here but not in go-to-sleep??

(describe henry)
(go-to-sleep henry)