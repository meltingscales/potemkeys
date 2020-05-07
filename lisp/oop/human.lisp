(defclass Person ()
  (
    (name       :initarg :name      :initform "Joe Schmoe"    :type string)
    (happiness  :initarg :happiness :initform 0               :type integer)
    (blue       :initarg :blue      :initform 0               :type integer)
  )
)

(defvar henry (make-instance 'Person :name "Henry Post"  :happiness 100  :blue 0 ))

(describe henry)