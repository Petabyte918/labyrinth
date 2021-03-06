#pragma once
//#include <compare>
#include <iostream>

namespace labyrinth {

class Location {
public:
    using IndexType = int16_t;
    struct OffsetType {
        using OffsetValueType = int16_t;
        explicit OffsetType(OffsetValueType row, OffsetValueType column) noexcept :
            row_offset{row}, column_offset{column} {}
        OffsetValueType row_offset{0};
        OffsetValueType column_offset{0};

        template <typename T>
        const OffsetType operator*(T scalar) const {
            return OffsetType{static_cast<OffsetValueType>(row_offset * scalar),
                              static_cast<OffsetValueType>(column_offset * scalar)};
        }
    };

    constexpr Location() noexcept : row_{-1}, column_{-1} {}

    template <typename T, typename U>
    constexpr explicit Location(T row, U column) noexcept :
        row_{static_cast<IndexType>(row)}, column_{static_cast<IndexType>(column)} {}

    const Location operator+(const OffsetType& offset) const noexcept;
    const Location operator-(const OffsetType& offset) const noexcept;
    const Location& operator+=(const OffsetType& offset) noexcept;
    const Location& operator-=(const OffsetType& offset) noexcept;

    IndexType getRow() const { // embind does not work with noexcept specifier
        return row_;
    }

    IndexType getColumn() const { // embind does not work with noexcept specifier
        return column_;
    }

    // auto operator<=>(const Location &) const = default;

    /* std::strong_ordering operator<=>(const Location & other) const {
        if (auto cmp = row_ <=> other.getRow(); cmp != 0) return cmp;
        return column_ <=> other.getColumn();
    } */

private:
    IndexType row_{0};
    IndexType column_{0};
};

inline bool operator==(const labyrinth::Location& lhs, const labyrinth::Location& rhs) noexcept {
    return lhs.getRow() == rhs.getRow() && lhs.getColumn() == rhs.getColumn();
}

inline bool operator!=(const labyrinth::Location& lhs, const labyrinth::Location& rhs) noexcept {
    return !(lhs == rhs);
}

inline bool operator<(const labyrinth::Location& lhs, const labyrinth::Location& rhs) noexcept {
    if (lhs.getRow() < rhs.getRow())
        return true;
    if (lhs.getRow() > rhs.getRow())
        return false;
    return lhs.getColumn() < rhs.getColumn();
}

} // namespace labyrinth

namespace std {
std::ostream& operator<<(std::ostream& stream, const labyrinth::Location& location);

template <>
struct hash<labyrinth::Location> {
    std::size_t operator()(labyrinth::Location const& location) const noexcept {
        std::size_t const row_hash{std::hash<std::size_t>{}(location.getRow())};
        std::size_t const column_hash{std::hash<std::size_t>{}(location.getColumn())};
        return row_hash ^ (column_hash << 1);
    }
};

} // namespace std
