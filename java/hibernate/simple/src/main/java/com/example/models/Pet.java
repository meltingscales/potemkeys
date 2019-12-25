package com.example.models;

import javax.persistence.*;

@Entity
@Table(name = "Pet")
public class Pet {

    @Id
    @GeneratedValue
    @Column(name = "pet_id")
    private int petID;

    @Column(name = "name")
    private String name;

    @Enumerated(EnumType.STRING)
    @Column(name = "pet_type")
    private PetType petType;

    @Override
    public String toString() {
        return "Pet{" +
                "petID=" + petID +
                ", name='" + name + '\'' +
                ", petType=" + petType +
                '}';
    }

    public Pet() {
    }

    public Pet(String name, int petId, PetType petType) {
        this.name = name;
        this.petID = petId;
        this.petType = petType;
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

    public PetType getPetType() {
        return petType;
    }

    public void setPetType(PetType petType) {
        this.petType = petType;
    }
}
