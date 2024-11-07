#include <iostream>
#include <memory>
#include <string>
#include <algorithm>
#include <vector>

using namespace std;

class StandardTriesNode
{
private:
    char m_Character;
    int m_WordEnd;
    shared_ptr<StandardTriesNode> m_Children[26] = {nullptr};

public:
    StandardTriesNode(char character) : m_Character(character), m_WordEnd(0) {}

    void AddChild(char character)
    {
        int index = character - 'A';
        if (index < 0 || index >= 26)
            return;

        if (m_Children[index] == nullptr)
        {
            m_Children[index] = make_shared<StandardTriesNode>(character);
        }
    }

    shared_ptr<StandardTriesNode> GetChild(char character)
    {
        int index = character - 'A';
        if (index < 0 || index >= 26)
            return nullptr;
        return m_Children[index];
    }

    void IncrementWordEnd()
    {
        m_WordEnd++;
    }

    void DecrementWordEnd()
    {
        m_WordEnd--;
    }

    int GetWordEndCount() const
    {
        return m_WordEnd;
    }

    bool HasChildren() const
    {
        for (const auto &child : m_Children)
        {
            if (child != nullptr)
                return true;
        }
        return false;
    }

    static bool Search(shared_ptr<StandardTriesNode> rootNode, const string &word)
    {
        shared_ptr<StandardTriesNode> currentNode = rootNode;

        for (char character : word)
        {
            currentNode = currentNode->GetChild(character);
            if (currentNode == nullptr)
                return false;
        }

        return currentNode->GetWordEndCount() > 0;
    }

    static void Insert(shared_ptr<StandardTriesNode> rootNode, const string &word)
    {
        shared_ptr<StandardTriesNode> currentNode = rootNode;

        for (char character : word)
        {
            currentNode->AddChild(character);
            currentNode = currentNode->GetChild(character);
        }

        currentNode->IncrementWordEnd();
    }

    static bool Delete(shared_ptr<StandardTriesNode> rootNode, const string &word)
    {
        shared_ptr<StandardTriesNode> currentNode = rootNode;

        for (char character : word)
        {
            currentNode = currentNode->GetChild(character);
            if (currentNode == nullptr)
                return false;
        }

        currentNode->DecrementWordEnd();
        return true;
    }
};

void DisplayMenu()
{
    cout << "Trie Menu:\n";
    cout << "1. Insert a word\n";
    cout << "2. Search for a word\n";
    cout << "3. Delete a word\n";
    cout << "4. Display all words\n";
    cout << "5. Exit\n";
    cout << "Choose an option: ";
}

void DisplayAllWords(shared_ptr<StandardTriesNode> rootNode, string currentWord, vector<string> &allWords)
{
    if (rootNode->GetWordEndCount() > 0)
    {
        allWords.push_back(currentWord);
    }

    for (char character = 'A'; character <= 'Z'; ++character)
    {
        shared_ptr<StandardTriesNode> child = rootNode->GetChild(character);
        if (child != nullptr)
        {
            DisplayAllWords(child, currentWord + character, allWords);
        }
    }
}

int main()
{
    auto rootNode = make_shared<StandardTriesNode>('\0');
    vector<string> basicWords = {"BAT", "BATMAN", "BATCAVE", "BANANA", "BALI", "BALL", "BASE"};

    for (const auto &word : basicWords)
    {
        StandardTriesNode::Insert(rootNode, word);
    }

    string word;

    while (true)
    {
        cin.clear();
        int choice;
        DisplayMenu();
        cin >> choice;
        vector<string> allWords;

        switch (choice)
        {
        case 1:
            cout << "Enter a word to insert: ";
            cin >> word;
            // Ensure the word is in uppercase
            transform(word.begin(), word.end(), word.begin(), ::toupper);
            StandardTriesNode::Insert(rootNode, word);
            cout << "Word inserted successfully!\n";
            break;
        case 2:
            cout << "Enter a word to search: ";
            cin >> word;
            transform(word.begin(), word.end(), word.begin(), ::toupper);
            if (StandardTriesNode::Search(rootNode, word))
            {
                cout << "Word found in the trie.\n";
            }
            else
            {
                cout << "Word not found in the trie.\n";
            }
            break;
        case 3:
            cout << "Enter a word to delete: ";
            cin >> word;
            transform(word.begin(), word.end(), word.begin(), ::toupper);
            if (StandardTriesNode::Delete(rootNode, word))
            {
                cout << "Word deleted successfully!\n";
            }
            else
            {
                cout << "Word not found in the trie.\n";
            }
            break;
        case 4:
            DisplayAllWords(rootNode, "", allWords);
            cout << "All words in the trie:\n";
            for (const auto &word : allWords)
            {
                cout << word << "\t";
            }
            cout << "\n";
            break;
        case 5:
            cout << "Exiting...\n";
            return 0;
        default:
            cout << "Invalid choice. Please try again.\n";
            return 0;
        }
    }

    return 0;
}