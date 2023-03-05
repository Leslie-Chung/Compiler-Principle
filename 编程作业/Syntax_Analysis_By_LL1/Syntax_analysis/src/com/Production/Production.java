package com.Production;

public class Production
{
    private Character left;
    private String right;

    public Production(Character left, String right)
    {
        this.left=left;
        this.right=right;

    }

    public Character getLeft()
    {
        return left;
    }

    public void setLeft(Character left)
    {
        this.left = left;
    }

    public String getRight()
    {
        return right;
    }

    public void setRight(String right)
    {
        this.right = right;
    }

    @Override
    public String toString() {
        return left.toString()+" -> "+right;
    }

    @Override
    public boolean equals(Object obj)
    {
        if (obj instanceof Production)
        {
            Production tmpProduction = (Production)obj;
            return tmpProduction.getLeft().equals(this.getLeft()) && tmpProduction.getRight().equals(this.getRight());
        }
        return super.equals(obj);
    }
}
