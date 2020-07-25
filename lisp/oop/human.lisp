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

(defmethod go-to-sleep ((obj Person))
  ; sleeping restores energy
  (setf (slot-value obj 'energy) 100)

  ; if they are an office worker, they lose their caffeine from sleeping
  (if (string-equal 'OfficeWorker (type-of obj))
    (setf (slot-value obj 'caffeine) 0))

  (format t "~s falls asleep. zzz...~%" (slot-value obj 'name))
)


(defclass OfficeWorker (Person)
  (
    (caffeine
      :initarg :caffeine
      :initform 100
      :type integer)
  )
)

(defmethod drink-coffee ((obj OfficeWorker))
  (setf (slot-value obj 'caffeine) 100)

  (format t "~s drinks a hot cup of joe. Mmm!~%" (slot-value obj 'name))
)


(defvar henry 
  (make-instance 'OfficeWorker 
    :name "Henry"
    :energy 0 ; needs to sleep :(
    :caffeine 50
  )
)

(go-to-sleep henry)   ; energy set to 100
(drink-coffee henry)  ; caffeine set to 100

(describe henry)