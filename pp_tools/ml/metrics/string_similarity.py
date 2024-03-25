
import jellyfish
import math
import nltk


class StringSimilarityMetrics:
    """
        - Jaccard index: The Jaccard index measures similarity between finite sets, which is calculated as the ratio of the size of the intersection of the sets to the size of the union of the sets.
        - Hamming distance: The Hamming distance between two strings of equal length is the number of positions at which the corresponding symbols are different.
        - Levenshtein distance: The Levenshtein distance between two strings is the minimum number of single-character edits (insertions, deletions, or substitutions) required to change one string into the other.
        - Cosine similarity: The Cosine similarity measures the cosine of the angle between two vectors in a high-dimensional space. For text documents, it can be used to compare the similarity of their term frequency vectors.
        - Overlap coefficient: The Overlap coefficient measures the size of the intersection of two sets relative to the size of the smaller set.
        - Sørensen–Dice coefficient: The Sørensen–Dice coefficient is a similarity measure that is the harmonic mean of the sizes of two sets, where the value is 1 if the two sets are identical and 0 if they have no common elements.
        - Ratcliff/Obershelp similarity: The Ratcliff/Obershelp similarity is a sequence matching algorithm that measures the similarity between two sequences of strings.
        - Monge-Elkan similarity: The Monge-Elkan similarity is a string similarity algorithm that calculates the average similarity between tokens in two strings. The similarity between two tokens is calculated using the Jaro-Winkler distance metric.
    """
    def __init__(self, str1, str2):
        self.str1 = str1
        self.str2 = str2
    
    def jaccard_index(self):
        set1 = set(self.str1.split())
        set2 = set(self.str2.split())
        intersection = set1.intersection(set2)
        union = set1.union(set2)
        return len(intersection) / len(union)
    
    def hamming_distance(self):
        if len(self.str1) != len(self.str2):
            raise ValueError("Strings must be of equal length")
        return sum(s1 != s2 for s1, s2 in zip(self.str1, self.str2))
    
    def levenshtein_distance(self):
        if len(self.str1) < len(self.str2):
            return self.levenshtein_distance(self.str2, self.str1)
        if len(self.str2) == 0:
            return len(self.str1)
        previous_row = range(len(self.str2) + 1)
        for i, s1 in enumerate(self.str1):
            current_row = [i + 1]
            for j, s2 in enumerate(self.str2):
                insertions = previous_row[j + 1] + 1
                deletions = current_row[j] + 1
                substitutions = previous_row[j] + (s1 != s2)
                current_row.append(min(insertions, deletions, substitutions))
            previous_row = current_row
        return previous_row[-1]
    
    def cosine_similarity(self):
        from collections import Counter
        def get_cosine(vec1, vec2):
            intersection = set(vec1.keys()) & set(vec2.keys())
            numerator = sum([vec1[x] * vec2[x] for x in intersection])
            sum1 = sum([vec1[x]**2 for x in vec1.keys()])
            sum2 = sum([vec2[x]**2 for x in vec2.keys()])
            denominator = math.sqrt(sum1) * math.sqrt(sum2)
            if not denominator:
                return 0.0
            else:
                return float(numerator) / denominator
        vec1 = Counter(self.str1.split())
        vec2 = Counter(self.str2.split())
        return get_cosine(vec1, vec2)
    
    def overlap_coefficient(self):
        set1 = set(self.str1.split())
        set2 = set(self.str2.split())
        overlap = set1.intersection(set2)
        return len(overlap) / min(len(set1), len(set2))
    
    def sorensen_dice_coefficient(self):
        set1 = set(self.str1)
        set2 = set(self.str2)
        overlap = len(set1.intersection(set2))
        return 2 * overlap / (len(set1) + len(set2))
    
    def ratcliff_obershelp_similarity(self):
        import difflib
        matcher = difflib.SequenceMatcher(None, self.str1, self.str2)
        return matcher.ratio()
    
    def monge_elkan_similarity(self):
        from nltk.tokenize import word_tokenize
        tokens1 = word_tokenize(self.str1)
        tokens2 = word_tokenize(self.str2)
        scores = []
        for token1 in tokens1:
            max_score = 0
            for token2 in tokens2:
                score = jellyfish.jaro_winkler(token1, token2)
                if score > max_score:
                    max_score = score
            scores.append(max_score)
        return sum(scores) / len(scores)

