package com.example.models;

import javax.persistence.*;

@Entity
@Table(name = "Pet", uniqueConstraints = {
        @UniqueConstraint(columnNames = "pet_id")
})
public class Pet {

    @Id
    @GeneratedValue
    @Column(name = "pet_id")
    private int petID;

    @Column(name = "name")
    private String name;

    public Pet() {
    }

    public Pet(String name, int id) {
        this.name = name;
        this.petID = id;
    }


    public int getPetID() {
        return petID;
    }

    public void setPetID(int petID) {
        this.petID = petID;
    }

    public String getName() {
        return name;
    }

    public void setName(String name) {
        this.name = name;
    }
}
